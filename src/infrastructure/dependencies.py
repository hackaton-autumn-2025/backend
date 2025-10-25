from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.database import db_manager
from src.infrastructure.http_client import HttpClient


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_manager.get_session():
        yield session

async def get_http_client() -> HttpClient:
    return HttpClient()

SessionDI = Annotated[AsyncSession, Depends(get_db)]
HttpClientDI = Annotated[HttpClient, Depends(get_http_client)]
