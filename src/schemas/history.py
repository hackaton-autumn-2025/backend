from datetime import time, datetime

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
    user_id: int