from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=100)


class UserUpdateRequest(BaseModel):
    name: str = Field(None, min_length=5, max_length=100)
    password: str = Field(None, min_length=8, max_length=100)


class UserResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
