import uuid
from typing import List, Optional

from pydantic import UUID4, BaseModel, EmailStr, Field


class UserEntity(BaseModel):
    id: Optional[UUID4] = Field(default=uuid.uuid4())
    email: EmailStr = Field(default_factory=EmailStr)
    password: str = Field(default_factory=str)
    roles: Optional[List[str]] = Field(default=[])
