from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, UUID4, Field


class RoleEnum(Enum):
    GUEST = 'guest'
    PUBLISHER = 'publisher'
    USER = 'user'
    ADMIN = 'admin'


class RoleEntity(BaseModel):
    name: Optional[str] = Field(default='guest')


class UserEntity(BaseModel):
    id: Optional[UUID4 | str] = Field(default_factory=uuid4)
    email: str
    password: Optional[str] = None
    roles: List[RoleEntity] = []

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = uuid4()