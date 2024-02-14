from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean

from src.database import Base

metadata = MetaData()

session_ = Table(
    'session',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('session_key', String, nullable=False),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('first_corp_number', Integer, nullable=False),
    Column('second_corp_number', Integer, nullable=False),
    Column('timestamp', TIMESTAMP, default=datetime.utcnow)
)

photo_ = Table(
    'photo',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('photo_name', String, nullable=False),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('timestamp', TIMESTAMP, default=datetime.utcnow)
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
