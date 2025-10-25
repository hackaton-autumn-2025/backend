from dataclasses import dataclass

from src.core.configs import settings
from src.core.security import create_jwt, get_password_hash, verify_password
from src.entities.user_dto import (
    CreateUserDTO,
    LoginDTO,
    TokenDTO,
    UpdateUserDTO,
    UserResponseDTO,
)
from src.enums import TokenType
from src.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistError,
    UserNotFoundError,
)
from src.repositories import UserRepository
from src.schemas import Token, UserResponse


@dataclass(kw_only=True, frozen=True, slots=True)
class UserService:
    repository: UserRepository

    async def register(self, user_dto: CreateUserDTO) -> UserResponse:
        if await self.repository.get_user_by_name(name=user_dto.name):
            raise UserAlreadyExistError(name=user_dto.name)
        user_dto.hashed_password = get_password_hash(password=user_dto.hashed_password)
        user_dto = await self.repository.create_user(user_dto)
        return UserResponse.model_validate(user_dto.__dict__)

    @staticmethod
    def __get_token_pair(user_id) -> TokenDTO:
        access_token = create_jwt(
            token_type=TokenType.ACCESS,
            subject=str(user_id),
        )
        refresh_token = create_jwt(
            token_type=TokenType.REFRESH,
            subject=str(user_id),
            expires_delta=settings.project_settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
        return TokenDTO(access_token, refresh_token)

    async def authenticate(self, login_dto: LoginDTO) -> Token:
        user = await self.repository.get_user_by_name(name=login_dto.name)
        if not user:
            raise UserNotFoundError(name=login_dto.name)
        if not verify_password(login_dto.password, user.hashed_password):
            raise InvalidCredentialsError()
        user_dto = UserResponseDTO.from_model(user)
        token_dto = self.__get_token_pair(user_id=user_dto.id)
        return Token.model_validate(token_dto.__dict__)

    async def get_user(self, user_id: int) -> UserResponse:
        user_dto = await self.repository.get_by_id(user_id)
        if not user_dto:
            raise UserNotFoundError(id=user_id)
        return UserResponse.model_validate(user_dto.__dict__)

    async def update_user(self, user_id, user_update_dto: UpdateUserDTO) -> UserResponse | None:
        if not user_update_dto.has_changes():
            return None
        if not await self.repository.get_by_id(user_id):
            raise UserNotFoundError(id=user_id)
        user_dto = await self.repository.update_user(user_id, user_update_dto)
        return UserResponse.model_validate(user_dto.__dict__)