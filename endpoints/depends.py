from db.base import database
from repositories.users import UserRepository


def get_user_repository() -> UserRepository:
    return UserRepository(database)
