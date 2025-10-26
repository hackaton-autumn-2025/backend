from pydantic import BaseModel

from src.schemas.route_schemas import Coordinate


class WayPointSchema(BaseModel):
    hint: str
    location: Coordinate
    name: str
    distance: float

class RoadNetworkResponseSchema(BaseModel):
    waypoints: list[WayPointSchema]


class 