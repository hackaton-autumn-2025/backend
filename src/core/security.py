from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.configs import settings
from src.enums import TokenType
from src.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login", refreshUrl="user/refresh")
refresh_scheme = HTTPBearer(auto_error=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_jwt(
    token_type: TokenType, subject: str, expires_delta: timedelta | None = None
) -> str:
    if not expires_delta:
        expires_delta = timedelta(
            minutes=settings.project_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    elif isinstance(expires_delta, int):
        expires_delta = timedelta(minutes=expires_delta)

    expire = datetime.now() + expires_delta
    to_encode = {"token_type": token_type.value, "sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.project_settings.SECRET_KEY)


def _decode_token_base(token: str, expected_type: TokenType) -> TokenData:
    try:
        payload = jwt.decode(token, settings.project_settings.SECRET_KEY)
        token_type = payload.get("token_type")

        if token_type != expected_type.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Неправильный тип токена {token_type}. Ожидался {expected_type}",
            )
        return TokenData(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        ) from None


def decode_access_token(token: str) -> TokenData:
    return _decode_token_base(token, TokenType.ACCESS)


def decode_refresh_token(token: str) -> TokenData:
    return _decode_token_base(token, TokenType.REFRESH)
