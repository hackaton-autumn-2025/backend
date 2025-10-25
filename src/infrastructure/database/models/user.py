from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SAenum
from sqlalchemy.orm import Mapped, mapped_column

from src.entities.user_dto import UserInternalDTO
from src.enums import UserRole
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.mixins.mixin import CreatedUpdatedMixin


class UserModel(Base, CreatedUpdatedMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAenum(UserRole), default=UserRole.USER.value, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def to_dto(self) -> UserInternalDTO:
        return UserInternalDTO(
            id=self.id,
            name=self.name,
            hashed_password=self.hashed_password,
            role=self.role,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
