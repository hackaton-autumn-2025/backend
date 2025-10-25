from fastapi import APIRouter, status

from src.controllers.dependencies.route_service import RouteServiceDI
from src.entities.route_dto import (
    RoutePointDTO,
    RoutesPointDTO,
)
from src.schemas.road_network_schemas import RoadNetworkResponseSchema
from src.schemas.route_schemas import (
    ListRouteRequestSchema,
)

router = APIRouter(prefix="/location", tags=["Расчет локации"])


@router.post(
    "/create_route",
    response_model=RoadNetworkResponseSchema,
    summary="Создать персональный маршрут",
    status_code=status.HTTP_200_OK,
)
async def create_route(users_routes: ListRouteRequestSchema, service: RouteServiceDI):
    routes_dto = [
        RoutesPointDTO(
            start_time=users_routes.start_time,
            transport_mode=users_routes.transport_mode,
            traffic_level=3,
            routes_point=[
                RoutePointDTO(
                    address=route.address,
                    lat=route.coordinate.lat,
                    lon=route.coordinate.lon,
                    work_start=route.work_start,
                    work_end=route.work_end,
                    lunch_start=route.lunch_start,
                    lunch_end=route.lunch_end,
                    stop_duration=route.stop_duration,
                    client_level=route.client_level,
                )
                for route in users_routes.routes_request
            ]
        )
    ]
    return await service.create_route(routes=routes_dto)

#
# @router.post(
#     "/create_route_demo",
#     response_model=RoutePointResponseSchema,
#     summary="Построение демонстрационного маршрута",
#     status_code=status.HTTP_200_OK,
# )
# async def create_demo_route(users_routes: list[RouteRequestKommivoyajerSchema], service: RouteServiceDI):
#     routes_dto = [
#         KommivoyajerRoutePointDTO(
#             address=route.address,
#             lat=route.coordinate.lat,
#             lon=route.coordinate.lon,
#             work_start=route.work_start,
#             work_end=route.work_end,
#             lunch_start=route.lunch_start,
#             lunch_end=route.lunch_end,
#             stop_duration=route.stop_duration
#         )
#         for route in users_routes
#     ]
