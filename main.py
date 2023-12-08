import os
import uuid
import json
from datetime import datetime
from hashlib import sha256

from PIL import Image

from fastapi import FastAPI, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from src.logging import logger_
from src.config import PATH_TO_PHOTOS
from src.database import get_async_session
from src.services import get_user_from_db, get_session_from_db, add_session_to_db, get_photo_from_db, add_photo_to_db
from src.utils import gen_fake_card, face_preprocess
from src.auth.base_config import auth_backend, fastapi_users, current_user, verified_user

from models.shemas import UserRead, UserCreate, User, Session, SessionCreate, SessionUserInput, PhotoCreate, CardData

app = FastAPI(
    title='FakeCardAPI'
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.post("/photo")
async def get_photo(file: UploadFile, user: User = Depends(verified_user),
                    session: AsyncSession = Depends(get_async_session)):
    content = await file.read()
    image: Image = face_preprocess(content)  # find face, cut  247 x 328
    if not image:
        # TO DO
        ...
    photo_name = f'{uuid.uuid4()}.{image.format.lower()}'

    image.save(os.path.join(PATH_TO_PHOTOS, photo_name))  # save photo in static/photo/photo_name

    new_photo = PhotoCreate(photo_name=photo_name, user_id=user.id)

    res = await add_photo_to_db(new_photo, session)  # write to db user.id, photo_name

    logger_.info(f'user: {user.id} | add photo | {str(res)} | photo_name: {photo_name}')
    return res


@app.post("/session")
async def create_session(new_session: SessionUserInput, user: User = Depends(verified_user),
                         session: AsyncSession = Depends(get_async_session)):

    data = {'user_id': user.id} | new_session.dict() | {"timestamp": datetime.utcnow().isoformat()}

    session_key = sha256(json.dumps(data, default=str).encode('utf-8')).hexdigest()
    data |= {'session_key': session_key}

    session_data = SessionCreate(**data)
    logger_.info(f'user: {user.id} | session created | {session_key}')

    result = await add_session_to_db(session_data, session)

    return result


@app.get("/pass", response_class=HTMLResponse)
async def get_card(request: Request, user: User = Depends(verified_user),
                   session: AsyncSession = Depends(get_async_session)):
    session_data = await get_session_from_db(user.id, session)
    photo_data = await get_photo_from_db(user.id, session)
    if not session_data or not photo_data:
        logger_.info(
            f'user: {user.id} | NOT FOUND | session_data: {session_data.dict()} | photo_data: {photo_data.dict()}\n')
        return templates.TemplateResponse('not_found.html', {"request": request})

    full_name = f'{session_data.last_name} {session_data.name[0]}.{session_data.surname[0]}.'

    card_data = CardData(**session_data.dict())

    card_path = gen_fake_card(card_data, photo_data.photo_name)
    card_path = card_path.split('\\')[-2:]
    card_path = '/' + '/'.join(card_path)
    logger_.info(f'user: {user.id} | card send | {session_data.session_key} | {photo_data.photo_name}\n')
    return templates.TemplateResponse("card.html", {"request": request, "full_name": full_name, "card_path": card_path})

# {{ url_for('static', path='/') }}
