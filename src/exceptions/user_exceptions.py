from src.exceptions.service_errors import (
    EntityAlreadyExistError,
    EntityNotFoundError,
    ServiceError,
)


class UserNotFoundError(EntityNotFoundError):
    entity_name = "Пользователь"


class UserAlreadyExistError(EntityAlreadyExistError):
    entity_name = "Пользователь"


class InvalidCredentialsError(ServiceError):
    def __init__(self, message: str = "Неверные учетные данные"):
        super().__init__(message)
