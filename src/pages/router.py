from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from src.logging import logger_
from src.database import get_async_session
from src.services import get_session_from_db, get_photo_from_db
from src.utils import gen_fake_card
from src.auth.base_config import current_user, current_active_user, verified_user

from models.shemas import User, CardData

router = APIRouter(
    prefix='',
    tags=['Pages']
)

templates = Jinja2Templates(directory="template")


@router.get('/')
async def get_home_page(request: Request, user: User = Depends(current_user)):
    who = True
    if not user:
        who = False
    return templates.TemplateResponse('home.html', {'request': request, 'who': who})


@router.get('/registration')
def get_register_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@router.get('/login')
def get_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get("/pass")
async def get_card_page(request: Request, user: User = Depends(verified_user),
                        session: AsyncSession = Depends(get_async_session)):
    session_data = await get_session_from_db(user.id, session)
    photo_data = await get_photo_from_db(user.id, session)
    if not session_data or not photo_data:
        logger_.info(
            f'user: {user.id} | NOT FOUND | session_data: {session_data.dict()} | photo_data: {photo_data.dict()}\n')
        return templates.TemplateResponse('404.html', {"request": request})

    full_name = f'{session_data.last_name} {session_data.name[0]}.{session_data.surname[0]}.'

    card_data = CardData(**session_data.dict())

    card_path = gen_fake_card(card_data, photo_data.photo_name)
    card_path = card_path.split('\\')[-2:]
    card_path = '/' + '/'.join(card_path)
    logger_.info(f'user: {user.id} | card send | {session_data.session_key} | {photo_data.photo_name}\n')
    return templates.TemplateResponse("card.html", {"request": request, "full_name": full_name, "card_path": card_path})
