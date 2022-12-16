import datetime

from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: str | None
    name: str
    email: EmailStr
    password: str
    is_company: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8, max_length=32)
    password2: str
    is_company: bool = False

    @validator("password2")
    def password_match(cls, value, values: dict, **kwargs):
        if 'password' in values and value != values.get('password'):
            raise ValueError("passwords don't match")
        return value

