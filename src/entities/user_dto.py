from dataclasses import dataclass
from datetime import datetime

from src.enums import UserRole


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
    id: int | None = None

    @classmethod
    def from_create_dto(
        cls,
        create_dto: CreateUserDTO,
        hashed_password: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> "UserInternalDTO":
        now = datetime.now()
        return cls(
            name=create_dto.name,
            hashed_password=hashed_password,
            role=create_dto.role,
            is_active=create_dto.is_active,
            created_at=created_at or now,
            updated_at=updated_at or now,
        )

    @classmethod
    def from_model(cls, user_model) -> "UserInternalDTO":
        return cls(
            id=user_model.id,
            name=user_model.name,
            hashed_password=user_model.hashed_password,
            role=user_model.role,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )


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
    password: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None

    def has_changes(self) -> bool:
        return any(
            (
                self.name is not None,
                self.password is not None,
                self.role is not None,
                self.is_active is not None,
            )
        )


@dataclass
class LoginDTO:
    name: str
    password: str


@dataclass
class TokenDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
