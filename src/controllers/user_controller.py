from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.controllers.dependencies.user_service import (
    CurrentUserDI,
    RefreshTokenDI,
    UserServiceDI,
)
from src.core.configs import settings
from src.core.security import create_jwt
from src.enums import TokenType
from src.exceptions.service_errors import ServiceError
from src.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistError,
    UserNotFoundError,
)
from src.schemas import Token, UserCreateRequest, UserResponse
from src.entities.user_dto import CreateUserDTO, LoginDTO

router = APIRouter(prefix="/user", tags=["Пользователь"])


@router.post(
    "",
    response_model=UserResponse,
    summary="Регистрация нового пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreateRequest,
    service: UserServiceDI,
):
    try:
        user_dto = CreateUserDTO(name=user_in.name, hashed_password=user_in.password)
        user = await service.register(user_dto)
        return user
    except UserAlreadyExistError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    "/login",
    response_model=Token,
    summary="Авторизация и получение JWT токенов",
    status_code=status.HTTP_200_OK,
)
async def login_for_access_token(
    service: UserServiceDI,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    try:
        login_dto = LoginDTO(name=form_data.username, password=form_data.password)
        return await service.authenticate(login_dto)
    except (UserNotFoundError, InvalidCredentialsError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Получить данные текущего авторизованного пользователя",
    status_code=status.HTTP_200_OK,
)
async def read_profile(
    current_user: CurrentUserDI,
):
    try:
        return current_user
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован или токен не действителен",
        ) from None


@router.post(
    "/refresh",
    response_model=Token,
    summary="Обновление пары access и refresh токенов",
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    token_data: RefreshTokenDI,
):
    new_access_token = create_jwt(
        token_type=TokenType.ACCESS,
        subject=token_data.sub,
    )
    new_refresh_token = create_jwt(
        token_type=TokenType.REFRESH,
        subject=token_data.sub,
        expires_delta=settings.project_settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )
