from fastapi import Depends

from sqlalchemy import select, insert, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DatabaseError

from fastapi_users.db import SQLAlchemyUserDatabase

from src.database import get_async_session
from models.models import user as user_table, session_ as session_table, photo_ as photo_table, User
from models.shemas import UserRead, Session, SessionCreate, Photo, PhotoCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_from_db(username: str, session: AsyncSession) -> UserRead or None:
    query = select(user_table).where(user_table.c.username == username)
    result = await session.execute(query)
    result = result.mappings().first()
    if result is not None:
        return UserRead(**result)


async def add_session_to_db(new_session: SessionCreate, session: AsyncSession):
    stmt = insert(session_table).values(**new_session.dict())
    try:
        await session.execute(stmt)
        await session.commit()
    except DatabaseError as error:
        print(error)
        return {"status": "error"}
    return {"status": "success"}


async def get_session_from_db(user_id: int, session: AsyncSession) -> Session or None:
    query = select(session_table).where(session_table.c.user_id == user_id).order_by(
        desc(session_table.c.timestamp)).limit(1)
    result = await session.execute(query)
    result = result.mappings().first()
    if result is not None:
        return Session(**result)


async def get_photo_from_db(user_id: int, session: AsyncSession) -> Photo or None:
    query = select(photo_table).where(photo_table.c.user_id == user_id).order_by(desc(photo_table.c.timestamp)).limit(1)
    result = await session.execute(query)
    result = result.mappings().first()
    if result is not None:
        return Photo(**result)


async def add_photo_to_db(new_photo: PhotoCreate, session: AsyncSession):
    stmt = insert(photo_table).values(**new_photo.dict())
    try:
        await session.execute(stmt)
        await session.commit()
    except DatabaseError as error:
        print(error)
        return {"status": "error"}
    return {"status": "success"}

# async def add_user_to_db(new_user: CreateUser, session: AsyncSession):
#     stmt = insert(user_).values(**new_user.dict())
#     try:
#         await session.execute(stmt)
#         await session.commit()
#     except DatabaseError as error:
#         print(error)
#         return {"status": "error"}
#     return {"status": "success"}
