import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.history import HistoryModel
from src.schemas.history import HistoryCreateSchema, HistoryResponseSchema


class HistoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = HistoryModel

    async def get_by_id(self, history_id: int) -> HistoryResponseSchema | None:
        history_model = await self._session.get(self.model, history_id)
        if history_model:
            history_dict = history_model.__dict__
            return HistoryResponseSchema.model_validate(history_dict)
        return None

    async def create(self, user_id, dto: HistoryCreateSchema) -> HistoryResponseSchema:
        routes_dict = [rp.model_dump() for rp in dto.routes_point]
        routes_json = json.dumps(routes_dict, default=str)
        serialized_routes = json.loads(routes_json)

        history_model = self.model(
            user_id=user_id,
            routes_point=serialized_routes,
            traffic_level=dto.traffic_level,
            transport_mode=dto.transport_mode.value,
            start_time=dto.start_time,
            arrival_times=dto.arrival_times,
            total_distance=dto.total_distance,
            total_time=dto.total_time
        )
        self._session.add(history_model)
        await self._session.commit()
        await self._session.refresh(history_model)
        history_dict = history_model.__dict__
        return HistoryResponseSchema.model_validate(history_dict)

    async def get_all(self, user_id: int) -> list[HistoryResponseSchema]:
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self._session.execute(query)
        histories = result.scalars().all()

        if not histories:
            return []

        return [HistoryResponseSchema.model_validate(history.__dict__) for history in histories]