from typing import List, Optional

from pydantic import BaseModel


class PermissionSchema(BaseModel):
    name: str


class RoleSchema(BaseModel):
    name: str
    permissions: List[PermissionSchema] = []


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    roles: Optional[List[RoleSchema]] = []


class UpdateUserPassword(BaseModel):
    password: str


class UserLogin(UserBase):
    password: str


class UserSchema(BaseModel):
    id: str
    email: str
    created_at: str
    updated_at: str

    roles: List[RoleSchema] = []
