from fastapi import APIRouter, status

from src.controllers.dependencies.history_service import HistoryServiceDI
from src.controllers.dependencies.user_service import CurrentUserDI
from src.schemas.history import HistoryCreateSchema, HistoryResponseSchema

router = APIRouter(prefix="/history", tags=["История"])


@router.post(
    "",
    response_model=HistoryResponseSchema,
    summary="Добавить в историю маршрутов",
    status_code=status.HTTP_201_CREATED,
)
async def create_history(current_user: CurrentUserDI, history_create: HistoryCreateSchema, service: HistoryServiceDI):
    return await service.create_history(current_user.id, history_create)

@router.get(
    "{history_id}",
    response_model=HistoryResponseSchema,
    summary="Посмотреть историю по id",
    status_code=status.HTTP_200_OK,
)
async def get_history_by_id(history_id: int, service: HistoryServiceDI):
    return await service.get_history_by_id(history_id)


@router.get(
    "/all",
    response_model=list[HistoryResponseSchema],
    summary="Посмотреть всю историю пользователя",
    status_code=status.HTTP_200_OK,
)
async def get_all_history(current_user: CurrentUserDI, service: HistoryServiceDI):
    return await service.get_all_history(current_user.id)


