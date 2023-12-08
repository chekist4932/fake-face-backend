import os
import io
import uuid
import json
from datetime import datetime
from hashlib import sha256
import logging

from PIL import Image

from fastapi import FastAPI, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import gen_fake_card, face_preprocess
from src.services import get_user_from_db, get_session_from_db, add_session_to_db, get_photo_from_db, add_photo_to_db
from models.shemas import UserRead, UserCreate, User, Session, SessionCreate, SessionUserInput, PhotoCreate, CardData
from src.auth.base_config import auth_backend, fastapi_users, current_user, verified_user
from src.database import get_async_session
from src.config import PATH_TO_PHOTOS

# name = __name__
# _log = logging.getLogger(name)
# _log.setLevel(logging.DEBUG)
# _log_handler = logging.FileHandler(filename=f'{name}.log',
#                                    encoding='utf-8',
#                                    mode="a")
# _log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
# _log_handler.setFormatter(_log_formatter)
# _log.addHandler(_log_handler)

app = FastAPI(
    title='Test API'
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


#
@app.get("/")
async def root(user: User = Depends(current_user)):
    return {"message": f"Hello, {user.username}"}


@app.post("/photo")
async def get_photo(file: UploadFile, user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    content = await file.read()
    # TO DO
    image: Image = face_preprocess(content)  # find face, cut  247 x 328
    if not image:
        ...
    photo_name = f'{uuid.uuid4()}.{image.format.lower()}'
    print(photo_name)
    image.save(os.path.join(PATH_TO_PHOTOS, photo_name))  # save photo in static/photo/photo_name
    new_photo = PhotoCreate(photo_name=photo_name, user_id=user.id)
    print(new_photo)
    res = await add_photo_to_db(new_photo, session)  # write to db user.id, photo_name
    return res | {'operation': 'add_photo'}

    # return {"message": f"Hello, {user.username}"}


@app.get("/username/{username}")
async def get_user(username: str, session: AsyncSession = Depends(get_async_session)):
    print("in function")
    result = await get_user_from_db(username, session=session)
    print(result)
    if result is not None:
        return {f'{username}': result.dict()}


@app.post("/session")
async def create_session(new_session: SessionUserInput, user: User = Depends(verified_user),
                         session: AsyncSession = Depends(get_async_session)):
    data = {'user_id': user.id} | new_session.dict() | {"timestamp": datetime.utcnow().isoformat()}

    session_key = sha256(json.dumps(data, default=str).encode('utf-8')).hexdigest()
    data |= {'session_key': session_key}

    session_data = SessionCreate(**data)
    print(f"Session created: {session_data}")

    result = await add_session_to_db(session_data, session)

    return result


@app.get("/pass", response_class=HTMLResponse)
async def get_card(request: Request, user: User = Depends(verified_user),
                   session: AsyncSession = Depends(get_async_session)):
    session_data = await get_session_from_db(user.id, session)
    photo_data = await get_photo_from_db(user.id, session)
    print(session_data)
    print(photo_data)
    if not session_data or not photo_data:
        return templates.TemplateResponse('not_found.html', {"request": request})

    full_name = f'{session_data.last_name} {session_data.name[0]}.{session_data.surname[0]}.'

    card_data = CardData(**session_data.dict())
    print(card_data)

    # TO DO
    card_path = gen_fake_card(card_data, photo_data.photo_name)
    card_path = card_path.split('\\')[-2:]
    card_path = '/' + '/'.join(card_path)
    # return templates.TemplateResponse("card.html", {"request": request, "full_name": full_name})
    return templates.TemplateResponse("card.html", {"request": request, "full_name": full_name, "card_path": card_path})

# {{ url_for('static', path='/') }}


# async def get_user(tg_id: int, session: AsyncSession) -> User_:
#     print('get')
#     query = select(user_).where(user_.c.tg_id == tg_id)
#     result = await session.execute(query)
#     result = result.first()
#     return result


# @app.post("/post_user/{tg_id}")
# async def get_user(new_user: CreateUser, session: AsyncSession = Depends(get_async_session)):
#     print("in function")
#     result = await add_user_to_db(new_user, session)
#     return result
