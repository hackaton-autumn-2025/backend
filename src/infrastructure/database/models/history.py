from datetime import time

from sqlalchemy import (
    JSON,
    ForeignKey,
    Time,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.entities.history_dto import HistoryDTO
from src.entities.route_dto import RoutePointDTO
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

    user = relationship("UserModel", back_populates="history")

    def to_dto(self) -> HistoryDTO:
        routes_point = [
            RoutePointDTO(**rp) for rp in self.routes_point
        ]
        return HistoryDTO(
            user_id=self.user_id,
            routes_point=routes_point,
            traffic_level=self.traffic_level,
            transport_mode=self.transport_mode,
            start_time=self.start_time,
        )