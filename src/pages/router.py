import json
import os
import uuid
from base64 import b64encode
from datetime import datetime
from hashlib import sha256

from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.shemas import User as User_shame, CardData, User, SessionCreate, SessionUserInput, PhotoCreate
from src.auth.base_config import current_active_user, verified_user
from src.config import PATH_TO_PHOTOS
from src.database import get_async_session
from src.my_logging import logger_
from src.services import get_session_from_db, get_photo_from_db, add_session_to_db, add_photo_to_db
from src.utils import gen_fake_card, face_preprocess

router = APIRouter(
    prefix='',
    tags=['Pages']
)

# templates = Jinja2Templates(directory="template")


@router.get('/welcome')
async def get_home_page():
    return JSONResponse(content={'message': 'Face-Drawer-Test'}, status_code=status.HTTP_200_OK)


@router.get('/users/me')
async def get_auth_status(user: User_shame = Depends(current_active_user)):
    return JSONResponse(content={'username': user.username}, status_code=status.HTTP_200_OK)


@router.post("/photo")
async def get_photo(file: UploadFile, user: User = Depends(verified_user),
                    session: AsyncSession = Depends(get_async_session)):
    try:
        content = await file.read()
        image: Image = face_preprocess(content)  # find face, cut  247 x 328
        if not image:
            # TO DO
            ...
    except Exception as er:
        print(er)
        return JSONResponse(content={"detail": "error"}, status_code=status.HTTP_400_BAD_REQUEST)

    photo_name = f'{uuid.uuid4()}.{image.format.lower()}'
    image.save(os.path.join(PATH_TO_PHOTOS, photo_name))  # save photo in static/photo/photo_name
    new_photo = PhotoCreate(photo_name=photo_name, user_id=user.id)

    try:
        res = await add_photo_to_db(new_photo, session)  # write to db user.id, photo_name
    except ValueError as er:
        return JSONResponse(content=er, status_code=status.HTTP_400_BAD_REQUEST)

    logger_.info(f'user: {user.id} | add photo | {str(res)} | photo_name: {photo_name}')
    return JSONResponse(content=res, status_code=status.HTTP_200_OK)


@router.post("/session")
async def create_session(new_session: SessionUserInput, user: User = Depends(verified_user),
                         session: AsyncSession = Depends(get_async_session)):
    data = {'user_id': user.id} | new_session.dict() | {"timestamp": datetime.utcnow().isoformat()}

    session_key = sha256(json.dumps(data, default=str).encode('utf-8')).hexdigest()
    data |= {'session_key': session_key}

    session_data = SessionCreate(**data)
    logger_.info(f'user: {user.id} | session created | {session_key}')

    try:
        result = await add_session_to_db(session_data, session)
    except ValueError as er:
        return JSONResponse(content=er, status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@router.get("/pass")
async def get_card_page(user: User_shame = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)):
    session_data = await get_session_from_db(user.id, session)
    photo_data = await get_photo_from_db(user.id, session)
    if not session_data or not photo_data:
        logger_.info(
            f'/PASS ERROR | data: {user} | session : {session_data}\n')
        return JSONResponse(content={"detail": 'Create session and/or Upload photo'},
                            status_code=status.HTTP_404_NOT_FOUND)
    # if is_exist('{PATH_TO_CARDS}/{session.session_key}'):
    # return b64encode(open('{PATH_TO_CARDS}/{session.session_key}', 'rb').read())

    full_name = f'{session_data.last_name} {session_data.name[0]}.{session_data.surname[0]}.'

    card_data = CardData(**session_data.dict())

    card_path = gen_fake_card(card_data, photo_data.photo_name)
    encoded_string = b64encode(open(card_path, "rb").read())
    card_in_base = 'data:image/png;base64,' + encoded_string.decode('utf-8')

    # logger_.info(f'user: {user.id} | card send | {session_data.session_key} | {photo_data.photo_name}\n')
    return JSONResponse(content={"full_name": full_name, 'card': card_in_base}, status_code=status.HTTP_200_OK)
