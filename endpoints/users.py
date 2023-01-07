from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from repositories.users import UserRepository
from models.user import User, UserIn
from .depends import get_user_repository, get_current_user


router = APIRouter()


@router.get("/", response_model=list[User])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        offset: int = 0,
):
    return await users.get_all(limit=limit, offset=offset)


@router.get("/by_email", response_model=User)
async def get_by_email(
        email: EmailStr,
        users: UserRepository = Depends(get_user_repository),
):
    return await users.get_by_email(email=email)


@router.post("/", response_model=User)
async def create_user(
        user_in: UserIn,
        users: UserRepository = Depends(get_user_repository),
):
    return await users.create(user_in=user_in)


@router.put("/", response_model=User)
async def update_user(
        user_id: int,
        user_in: UserIn,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user),
) -> User:
    old_user = await users.get_by_id(user_id=user_id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await users.update(user_id=user_id, ui=user_in)
