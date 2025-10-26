from dataclasses import dataclass
from typing import Any

from src.core.configs import settings
from src.entities.route_dto import RoutesPointDTO
from src.infrastructure.dependencies import HttpClientDI
from src.schemas.road_network_schemas import RoadNetworkResponseSchema, WayPointSchema
from src.schemas.route_schemas import Coordinate, RoutePointResponseSchema
from src.utils import prepare_optimize_route_data


@dataclass(kw_only=True, frozen=True, slots=True)
class RouteService:
    _http_client: HttpClientDI

    async def create_route(self, routes: RoutesPointDTO) -> RoadNetworkResponseSchema:
        points = await self.__get_route_by_neyro(routes)
        road_marking = await self.__get_road_markings(points=points)
        return road_marking

    async def create_demo_route(self) -> dict[str, Any]:
        points = await self.__get_demo_route_by_neyro()
        road_marking = await self.__get_road_markings(points=points)
        return road_marking

    async def __get_route_by_neyro(self, routes: RoutesPointDTO) -> RoutePointResponseSchema:
        route_payload = prepare_optimize_route_data(routes)
        response = await self._http_client.post(
            url=settings.infra_settings.NEYRO_API,
            json=route_payload
        )
        return RoutePointResponseSchema.model_validate(response)

    async def __get_demo_route_by_neyro(self) -> RoutePointResponseSchema:
        response = await self._http_client.get(
            url=settings.infra_settings.NEYRO_DEMO,
        )
        return RoutePointResponseSchema.model_validate(response)

    async def __get_road_markings(self, points: RoutePointResponseSchema) -> RoadNetworkResponseSchema:
        points = points.model_dump()
        route_coordinates = points.get("route_coordinates")
        coords_str = ";".join(f"{p['lon']},{p['lat']}" for p in route_coordinates)

        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "true",
            "annotations": "true"
        }

        response = await self._http_client.get(
            url=f"{settings.infra_settings.ROAD_NETWORK_API}{coords_str}",
            params=params
        )

        waypoints_data = [
            WayPointSchema(
                hint=wp["hint"],
                location=Coordinate(lat=wp["location"][1], lon=wp["location"][0]),
                name=wp["name"],
                distance=wp["distance"]
            )
            for wp in response["waypoints"]
        ]
        arrival_times = points.get("arrival_times")
        total_distance = points.get("total_distance")
        total_time = points.get("total_time")

        return RoadNetworkResponseSchema(waypoints=waypoints_data, arrival_times=arrival_times, total_distance=total_distance, total_time=total_time)

