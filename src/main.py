import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.database import db_manager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.configs import settings
from src.core.exception import setup_exception_handlers
from src.core.log import logger
from src.core.middleware import setup_middleware
from src.core.routers import setup_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application...")

    logger.info("FastAPI application started successfully")
    db_manager.init()
    await db_manager.create_tables()
    yield
    await db_manager.close()
    logger.info("FastAPI application shutdown complete")


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_settings.PROJECT_NAME,
        version=settings.project_settings.VERSION,
        lifespan=lifespan,
    )

    setup_middleware(application)

    setup_routers(application)

    setup_exception_handlers(application)

    return application


app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.project_settings.HOST,
        port=settings.project_settings.PORT,
        log_level=settings.log_settings.LOG_LEVEL,
        access_log=settings.log_settings.ACCESS_LOG,
    )
