from dataclasses import dataclass

from src.exceptions.history_exceptions import HistoryNotFoundError
from src.repositories.history_repo import HistoryRepository
from src.schemas.history import HistoryResponseSchema, HistoryCreateSchema


@dataclass(kw_only=True, frozen=True, slots=True)
class HistoryService:
    repository: HistoryRepository

    async def create_history(self, user_id, history_dto: HistoryCreateSchema) -> HistoryResponseSchema:
        return await self.repository.create(user_id, history_dto)

    async def get_history_by_id(self, history_id: int) -> HistoryResponseSchema:
        history = await self.repository.get_by_id(history_id)
        if not history:
            raise HistoryNotFoundError(id=history_id)
        return history

    async def get_all_history(self, user_id: int) -> list[HistoryResponseSchema]:
        histories = await self.repository.get_all(user_id)

        return histories