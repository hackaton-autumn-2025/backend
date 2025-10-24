import time

from fastapi import FastAPI

from src import controllers


def setup_routers(application: FastAPI) -> None:
    @application.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "healthy", "timestamp": f"{time.time()}"}

    for router in controllers.__all__:
        application.include_router(getattr(controllers, router))
