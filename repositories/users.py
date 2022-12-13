from db import users
from models.user import User, UserIn
from .base import BaseRepository


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> list[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def get_by_id(self, user_id: int) -> User | None:
        query = users.select().where(users.c.id == user_id).first()
        user = await self.database.fetch_one(query)
        if not user:
            return None
        return User.parse_obj(user)

    async def get_by_email(self, email: str) -> User | None:
        query = users.select().where(users.c.id == email).first()
        user = await self.database.fetch_one(query)
        if not user:
            return None
        return User.parse_obj(user)

    async def create(self, ui: UserIn) -> User:
        return

    async def update(self, ui: UserIn) -> User:
        return
