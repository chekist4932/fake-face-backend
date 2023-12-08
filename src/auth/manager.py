from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from models.models import User
from src.services import get_user_db
from src.config import SECRET_AUTH
from src.logging import logger_


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger_.info(f'user: {user.id} | registration success | {user.username}')

    async def on_after_login(self, user: User, request: Optional[Request] = None, response: Optional[Response] = None):
        logger_.info(f'user: {user.id} | login success | {user.username}')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)