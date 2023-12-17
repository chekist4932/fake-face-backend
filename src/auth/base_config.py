from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from src.auth.manager import get_user_manager
from models.models import User
from src.config import PUBLIC_KEY_PATH, PRIVATE_KEY_PATH, ALGORITHM

bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=PRIVATE_KEY_PATH.read_text(),
                       lifetime_seconds=3600,
                       algorithm=ALGORITHM,
                       public_key=PUBLIC_KEY_PATH.read_text())


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(optional=True)
current_active_user = fastapi_users.current_user(active=True)
admin = fastapi_users.current_user(active=True, superuser=True)
verified_user = fastapi_users.current_user(active=True, verified=True)
