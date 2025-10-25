from typing import Annotated

from fastapi import Depends

from src.infrastructure.dependencies import SessionDI
from src.repositories.history_repo import HistoryRepository
from src.services.history_service import HistoryService


async def get_history_service(session: SessionDI) -> HistoryService:
    return HistoryService(repository=HistoryRepository(session=session))


HistoryServiceDI = Annotated[HistoryService, Depends(get_history_service)]
