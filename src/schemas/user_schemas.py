from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=100)


class UserUpdateRequest(BaseModel):
    name: str = Field(None, min_length=5, max_length=100)
    work_start: time = Field(None)
    work_end: time = Field(None)
    lunch_start: time = Field(None)
    lunch_end: time = Field(None)

class UserResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    work_start: time | None = None
    work_end: time | None = None
    lunch_start: time | None = None
    lunch_end: time | None = None

    model_config = ConfigDict(from_attributes=True)
