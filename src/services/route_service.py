from dataclasses import asdict, dataclass

from fastapi.encoders import jsonable_encoder

from src.core.configs import settings
from src.entities.route_dto import RoutesPointDTO
from src.infrastructure.dependencies import HttpClientDI
from src.schemas.road_network_schemas import RoadNetworkResponseSchema, WayPointSchema
from src.schemas.route_schemas import Coordinate, RoutePointResponseSchema


@dataclass(kw_only=True, frozen=True, slots=True)
class RouteService:
    _http_client: HttpClientDI

    async def create_route(self, routes: RoutesPointDTO) -> RoadNetworkResponseSchema:
        coordinates = [
            Coordinate(lat=point.lat, lon=point.lon)
            for point in routes.routes_point
            if point.lat is not None and point.lon is not None
        ]

        points = RoutePointResponseSchema(ordered_coordinates=coordinates)
        road_marking = await self.__get_road_markings(points=points)
        return road_marking

    async def __get_route_by_neyro(self, routes: RoutesPointDTO) -> RoutePointResponseSchema:
        route_payload = jsonable_encoder([asdict(r) for r in routes])

        response = await self._http_client.post(
            url=settings.infra_settings.NEYRO_API,
            json=route_payload
        )
        return RoutePointResponseSchema.model_validate(response)

    async def __get_road_markings(self, points: RoutePointResponseSchema) -> RoadNetworkResponseSchema:
        points = points.model_dump()
        ordered_coordinates = points.get("ordered_coordinates")
        coords_str = ";".join(f"{p['lon']},{p['lat']}" for p in ordered_coordinates)

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

        return RoadNetworkResponseSchema(waypoints=waypoints_data)
