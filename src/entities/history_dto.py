from dataclasses import dataclass
from datetime import time

from src.entities.route_dto import RoutePointDTO
from src.enums.route import TransportMode


@dataclass
class HistoryDTO:
    user_id: int
    routes_point: list[RoutePointDTO]
    traffic_level: int
    transport_mode: TransportMode
    start_time: time

    def __post_init__(self):
        if not (1 <= self.traffic_level <= 10):
            raise ValueError("traffic_level должен быть между 1 и 10")