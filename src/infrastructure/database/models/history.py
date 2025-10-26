from datetime import datetime, time

from sqlalchemy import JSON, ForeignKey, Integer, Time, func
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.enums.route import TransportMode
from src.infrastructure.database.base import Base


class HistoryModel(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    routes_point: Mapped[dict] = mapped_column(JSON, nullable=False)
    traffic_level: Mapped[int] = mapped_column(nullable=False)
    transport_mode: Mapped[TransportMode] = mapped_column(SAEnum(TransportMode), nullable=False)

    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    current_date: Mapped[datetime] = mapped_column(server_default=func.now(),nullable=False)
    arrival_times: Mapped[dict] = mapped_column(JSON, nullable=True)
    total_distance: Mapped[float] = mapped_column(nullable=True)
    total_time: Mapped[float] = mapped_column(Integer, nullable=True)
    user = relationship("UserModel", back_populates="history")