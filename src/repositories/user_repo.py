from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.user_dto import CreateUserDTO, UpdateUserDTO, UserInternalDTO
from src.infrastructure.database.models import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = UserModel

    async def get_by_id(self, user_id: int) -> UserInternalDTO | None:
        user_model = await self._session.get(self.model, user_id)
        if user_model:
            return self.model.to_dto(user_model)
        return None

    async def create_user(self, dto: CreateUserDTO) -> UserInternalDTO:
        user_model = self.model(**vars(dto))
        self._session.add(user_model)
        await self._session.commit()
        await self._session.refresh(user_model)
        return self.model.to_dto(user_model)

    async def get_user_by_name(self, name: str) -> UserInternalDTO | None:
        result = await self._session.execute(
            select(self.model).where(self.model.name == name)
        )
        user_model = result.scalar()
        if user_model:
            return self.model.to_dto(user_model)
        return None

    async def update_user(self, user_id: int, user_update: UpdateUserDTO) -> UserInternalDTO | None:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(**vars(user_update))
        )
        await self._session.execute(stmt)
        await self._session.commit()

        user_model = await self._session.get(self.model, user_id)
        if user_model:
            return self.model.to_dto(user_model)
        return None
