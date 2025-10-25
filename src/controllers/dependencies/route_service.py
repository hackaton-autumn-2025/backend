from typing import Annotated

from fastapi import Depends

from src.infrastructure.dependencies import get_http_client
from src.infrastructure.http_client import HttpClient
from src.services.route_service import RouteService


async def get_route_service(http_client: HttpClient = Depends(get_http_client)) -> RouteService:
    return RouteService(_http_client=http_client)


RouteServiceDI = Annotated[RouteService, Depends(get_route_service)]
