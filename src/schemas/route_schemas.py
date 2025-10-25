from datetime import time

from pydantic import BaseModel

from src.enums.route import ClientLevel, TransportMode


class Coordinate(BaseModel):
    lat: float
    lon: float


class RouteSchema(BaseModel):
    address: str
    coordinate: Coordinate
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
    ordered_coordinates: list[Coordinate]

