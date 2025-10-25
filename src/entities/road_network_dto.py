from dataclasses import dataclass
from typing import Any


@dataclass
class RoadNetworkResponseDTO:
    waypoints: list[dict[str, Any]]