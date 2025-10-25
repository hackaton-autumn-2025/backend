from dataclasses import asdict, dataclass, is_dataclass
from datetime import time

from src.enums.route import ClientLevel, TransportMode
from src.schemas.route_schemas import Coordinate


def to_jsonable(obj):
    if is_dataclass(obj):
        return {k: to_jsonable(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [to_jsonable(v) for v in obj]
    elif isinstance(obj, time):
        return obj.strftime("%H:%M:%S")
    else:
        return obj

@dataclass
class RouteBaseDTO:
    address: str
    lat: float
    lon: float
    work_start: time
    work_end: time
    lunch_start: time
    lunch_end: time
    stop_duration: time


@dataclass
class KommivoyajerRoutePointDTO(RouteBaseDTO):
    pass


@dataclass
class RoutePointDTO(RouteBaseDTO):
    client_level: ClientLevel


@dataclass
class RoutesPointDTO:
    routes_point: list[RoutePointDTO]
    traffic_level: int
    transport_mode: TransportMode
    start_time: time

    def __post_init__(self):
        if not (1 <= self.traffic_level <= 10):
            raise ValueError("level_route должен быть между 1-10")

@dataclass
class RoutePointResponseDTO:
    ordered_coordinates: list[Coordinate]
