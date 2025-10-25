from datetime import time

from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SAenum
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    work_start: Mapped[time] = mapped_column(default=time(9, 0))
    work_end: Mapped[time] = mapped_column(default=time(18, 0))
    lunch_start: Mapped[time] = mapped_column(nullable=True)
    lunch_end: Mapped[time] = mapped_column(nullable=True)

    history = relationship(
        "HistoryModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def to_dto(self) -> UserInternalDTO:
        return UserInternalDTO(
            id=self.id,
            name=self.name,
            hashed_password=self.hashed_password,
            role=self.role,
            is_active=self.is_active,
            work_start=self.work_start,
            work_end=self.work_end,
            lunch_start=self.lunch_start,
            lunch_end=self.lunch_end,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )