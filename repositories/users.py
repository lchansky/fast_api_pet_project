import datetime

import asyncpg
from fastapi import HTTPException, status

from core.security import hash_password
from db import users
from models.user import User, UserIn
from .base import BaseRepository


class UserRepository(BaseRepository):

    async def create(self, user_in: UserIn) -> User:
        dt_now = datetime.datetime.utcnow()
        user = User(
            name=user_in.name,
            email=user_in.email,
            password=hash_password(user_in.password),
            is_company=user_in.is_company,
            created_at=dt_now,
            updated_at=dt_now,
        )
        user_kwargs = user.dict()
        user_kwargs.pop('id')

        query = users.insert().values(user_kwargs)

        try:
            user.id = await self.database.execute(query)
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'This email already exists')

        user.password = ''
        return user

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[User]:
        query = users.select().limit(limit).offset(offset)
        return await self.database.fetch_all(query)

    async def get_by_id(self, user_id: int) -> User | None:
        query = users.select().where(users.c.id == user_id)
        user = await self.database.fetch_one(query)
        if not user:
            return None
        return User.parse_obj(user)

    async def get_by_email(self, email: str) -> User | None:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if not user:
            return None
        return User.parse_obj(user)

    async def update(self, user_id: int, ui: UserIn) -> User:
        dt_now = datetime.datetime.utcnow()
        user = User(
            id=user_id,
            name=ui.name,
            email=ui.email,
            password=hash_password(ui.password),
            is_company=ui.is_company,
            updated_at=dt_now,
        )
        user_kwargs = user.dict()
        user_kwargs.pop('created_at')
        user_kwargs.pop('id')

        query = users.update().where(users.c.id == user_id).values(user_kwargs)
        await self.database.execute(query)
        return user
