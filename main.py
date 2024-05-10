from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.models.shemas import UserRead, UserCreate
from src.auth.base_config import auth_backend, fastapi_users
from src.pages.router import router as router_pages

app = FastAPI(
    title='FakeCardAPI'
)

app.mount("/static", StaticFiles(directory="static"), name="static")

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

app.include_router(router_pages)

# origins = [
#     "http://localhost:3000",
#     "https://0f5d-77-35-31-20.ngrok-free.app/",
# ]
origins = [
    "http://213.139.210.94",
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

# @app.get("/pass", response_class=HTMLResponse)
# async def get_card(request: Request, user: User = Depends(verified_user),
#                    session: AsyncSession = Depends(get_async_session)):
#     session_data = await get_session_from_db(user.id, session)
#     photo_data = await get_photo_from_db(user.id, session)
#     if not session_data or not photo_data:
#         logger_.info(
#             f'user: {user.id} | NOT FOUND | session_data: {session_data.dict()} | photo_data: {photo_data.dict()}\n')
#         return templates.TemplateResponse('404.html', {"request": request})
#
#     full_name = f'{session_data.last_name} {session_data.name[0]}.{session_data.surname[0]}.'
#
#     card_data = CardData(**session_data.dict())
#
#     card_path = gen_fake_card(card_data, photo_data.photo_name)
#     card_path = card_path.split('\\')[-2:]
#     card_path = '/' + '/'.join(card_path)
#     logger_.info(f'user: {user.id} | card send | {session_data.session_key} | {photo_data.photo_name}\n')
#     return templates.TemplateResponse("card.html", {"request": request, "full_name": full_name, "card_path": card_path})

# {{ url_for('static', path='/') }}
