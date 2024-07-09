from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UpdateUserPassword(BaseModel):
    password: str


class UserSchema(BaseModel):
    id: str
    email: str
    created_at: str
    updated_at: str

    roles: List
