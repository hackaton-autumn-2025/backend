from dataclasses import dataclass
from datetime import datetime, time

from src.enums import UserRole
from src.schemas import UserUpdateRequest


@dataclass
class CreateUserDTO:
    name: str
    hashed_password: str
    role: UserRole = UserRole.USER
    is_active: bool = True


@dataclass
class UserInternalDTO:
    name: str
    hashed_password: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    work_start: time
    work_end: time
    id: int | None = None
    lunch_start: time | None = None
    lunch_end: time | None = None


@dataclass
class UserResponseDTO:
    id: int
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, user_model) -> "UserResponseDTO":
        return cls(
            id=user_model.id,
            name=user_model.name,
            role=user_model.role,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )


@dataclass
class UpdateUserDTO:
    name: str | None = None

    work_start: time | None = None
    work_end: time | None = None
    lunch_start: time | None = None
    lunch_end: time | None = None

    def has_changes(self) -> bool:
        return any(
            (
                self.name is not None,
                self.work_start is not None,
                self.work_end is not None,
                self.lunch_start is not None,
                self.lunch_end is not None

            )
        )

    def get_update_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class LoginDTO:
    name: str
    password: str


@dataclass
class TokenDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
