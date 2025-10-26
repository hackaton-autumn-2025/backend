from datetime import datetime, time
from random import randint
from typing import Any

from src.entities.route_dto import RoutesPointDTO
from src.enums.route import ClientLevel


def get_traffic_level_by_time() -> int:
    hour = datetime.now().time().hour
    return randint(
        (8 if 7 <= hour < 10 else
         7 if 17 <= hour < 20 else
         5 if 12 <= hour < 14 else
         1 if 23 <= hour or hour < 6 else 4),
        (10 if 7 <= hour < 10 else
         9 if 17 <= hour < 20 else
         7 if 12 <= hour < 14 else
         3 if 23 <= hour or hour < 6 else 6)
    )


def prepare_optimize_route_data(routes_dto: RoutesPointDTO) -> dict[str, Any]:
    def format_time(t: time | None) -> str | None:
        if not t:
            return None
        return t.strftime("%H:%M")

    def format_stop_duration(duration: time | int | str) -> int:
        if isinstance(duration, time):

            return duration.hour * 60 + duration.minute
        elif isinstance(duration, str):

            try:

                if ':' in duration:
                    parts = duration.split(':')
                    if len(parts) >= 2:
                        hours = int(parts[0])
                        minutes = int(parts[1])
                        return hours * 60 + minutes

                return int(duration)
            except (ValueError, AttributeError):
                return 0
        elif isinstance(duration, int):

            return duration
        else:
            return 0

    points = []
    for count, point in enumerate(routes_dto.routes_point):
        client_level = point.client_level.value
        client_level = client_level.capitalize() if client_level != ClientLevel.VIP.value else client_level
        points.append({
            "id": count,
            "address": point.address,
            "latitude": point.lat,
            "longitude": point.lon,
            "work_start": format_time(point.work_start),
            "work_end": format_time(point.work_end),
            "lunch_start": format_time(point.lunch_start),
            "lunch_end": format_time(point.lunch_end),
            "stop_duration": format_stop_duration(point.stop_duration),
            "client_level": client_level
        })

    return {
        "points": points,
        "traffic_level": routes_dto.traffic_level,
        "transport_mode": routes_dto.transport_mode.value.lower(),
        "start_time": format_time(routes_dto.start_time),
        "start_point": [points[0]["latitude"], points[0]["longitude"]] if points else [0, 0]
    }