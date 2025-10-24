from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from src.core.security import (
    decode_access_token,
    decode_refresh_token,
    oauth2_scheme,
    refresh_scheme,
)
from src.enums import UserRole
from src.infrastructure.dependencies import SessionDI
from src.repositories import UserRepository
from src.schemas import TokenData, UserResponse
from src.services.user_service import UserService


async def get_user_service(session: SessionDI) -> UserService:
    return UserService(repository=UserRepository(session))


async def get_current_access_token(
    token: str = Depends(oauth2_scheme),
) -> TokenData:
    token_data = decode_access_token(token)

    return token_data


async def get_current_refresh_token(
    token: HTTPBearer = Depends(refresh_scheme),
) -> TokenData:
    token = token.credentials
    token_data = decode_refresh_token(token)
    return token_data


async def get_current_user(
    token_data: "AccessTokenDI",
    service: "UserServiceDI",
) -> UserResponse:
    return await service.get_user(int(token_data.sub))


async def get_current_admin(
    current_user: "CurrentUserDI",
) -> UserResponse:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не является админом",
        )

    return current_user


CurrentUserDI = Annotated[UserResponse, Depends(get_current_user)]
CurrentAdminDI = Annotated[UserResponse, Depends(get_current_admin)]
UserServiceDI = Annotated[UserService, Depends(get_user_service)]
AccessTokenDI = Annotated[TokenData, Depends(get_current_access_token)]
RefreshTokenDI = Annotated[TokenData, Depends(get_current_refresh_token)]
