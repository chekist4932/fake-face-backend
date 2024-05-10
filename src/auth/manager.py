from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.models.models import User
from src.config import PRIVATE_KEY_PATH
from src.my_logging import logger_
from src.services import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = PRIVATE_KEY_PATH.read_text()
    verification_token_secret = PRIVATE_KEY_PATH.read_text()

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger_.info(f'user: {user.id} | registration success | {user.username}')

    async def on_after_login(self, user: User, request: Optional[Request] = None, response: Optional[Response] = None):
        logger_.info(f'user: {user.id} | login success | {user.username}')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
