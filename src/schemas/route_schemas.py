from datetime import time

from pydantic import BaseModel, Field, field_validator

from src.enums.route import ClientLevel, TransportMode


class Coordinate(BaseModel):
    lat: float
    lon: float


class RouteSchema(BaseModel):
    address: str
    coordinate: Coordinate | None = Field(None)
    work_start: time
    work_end: time
    lunch_start: time
    lunch_end: time
    stop_duration: time

class RouteRequestKommivoyajerSchema(RouteSchema):
    pass

class RouteRequestSchema(RouteSchema):
    client_level: ClientLevel

class ListRouteRequestSchema(BaseModel):
    routes_request: list[RouteRequestSchema]
    transport_mode: TransportMode
    start_time: time

class RoutePointResponseSchema(BaseModel):
    route_coordinates: list[Coordinate]
    arrival_times: list[str]
    total_distance: float
    total_time: float

    @field_validator('route_coordinates', mode='before')
    def validate_route_coordinates(cls, v):
        if isinstance(v, list) and v and isinstance(v[0], list):
            return [Coordinate(lat=coord[0], lon=coord[1]) for coord in v]
        return v