from datetime import time

from pydantic import BaseModel, Field, field_validator, model_validator

from src.enums.route import ClientLevel, TransportMode


class Coordinate(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class RouteSchema(BaseModel):
    address: str
    coordinate: Coordinate | None = Field(None)
    work_start: time
    work_end: time
    lunch_start: time
    lunch_end: time
    stop_duration: time

    @model_validator(mode='after')
    def validate_time_logic(self):

        if self.work_start >= self.work_end:
            raise ValueError('Время начала работы должно быть раньше времени окончания')

        if self.lunch_start >= self.lunch_end:
            raise ValueError('Время начала обеда должно быть раньше времени окончания')

        if not (self.work_start <= self.lunch_start <= self.lunch_end <= self.work_end):
            raise ValueError('Обеденное время должно быть в пределах рабочего времени')

        return self

    @field_validator('stop_duration')
    def validate_stop_duration(cls, v):
        total_seconds = v.hour * 3600 + v.minute * 60 + v.second
        if total_seconds < 60:
            raise ValueError("Длительность остановки должна быть больше 1 минуты")
        return v


class RouteRequestKommivoyajerSchema(RouteSchema):
    pass

class RouteRequestSchema(RouteSchema):
    client_level: ClientLevel

class ListRouteRequestSchema(BaseModel):
    routes_request: list[RouteRequestSchema]
    transport_mode: TransportMode
    start_time: time

    @field_validator('routes_request')
    def validate_routes_count(cls, v):
        if len(v) < 2:
            raise ValueError("Список маршрутов должен содержать 2 элемента")
        return v

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
