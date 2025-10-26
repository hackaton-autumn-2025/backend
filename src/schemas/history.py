from datetime import datetime, time

from pydantic import BaseModel, conint

from src.enums.route import TransportMode
from src.schemas.route_schemas import RouteRequestSchema


class BaseHistorySchema(BaseModel):
    routes_point: list[RouteRequestSchema]
    traffic_level: conint(ge=1, le=10)
    transport_mode: TransportMode
    start_time: time
    current_date: datetime
    arrival_times: list[str]
    total_distance: float
    total_time: float

class HistoryCreateSchema(BaseHistorySchema):
    pass

class HistoryResponseSchema(BaseHistorySchema):
    id: int
    user_id: int
    current_date: datetime | None
    arrival_times: list[str] | None
    total_distance: float | None
    total_time: float | None