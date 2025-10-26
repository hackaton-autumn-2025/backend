import traceback

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.log import logger
from src.exceptions.service_errors import EntityAlreadyExistError, EntityNotFoundError


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EntityAlreadyExistError)
    async def entity_already_exists_handler(
        request: Request, exc: EntityAlreadyExistError
    ):
        logger.warning(f"EntityAlreadyExistsError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": jsonable_encoder(exc)},
        )

    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_handler(request: Request, exc: EntityAlreadyExistError):
        logger.warning(f"EntityNotFoundError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": jsonable_encoder(exc)},
        )


    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        logger.warning(f"ValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Validation Error",
                "errors": jsonable_encoder(exc.errors()),
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        tb = traceback.format_exc()
        logger.error(f"SQLAlchemyError: {exc!s}\nTraceback:\n{tb}")
        if isinstance(exc, IntegrityError):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "detail": "Database integrity error",
                    "errors": (str(exc.orig) if hasattr(exc, "orig") else str(exc)),
                },
            )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "Database error",
                "errors": str(exc),
            },
        )

    @app.exception_handler(JWTError)
    async def jwt_exception_handler(request: Request, exc: JWTError):
        logger.warning(f"JWTError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid token"},
            headers={"WWW-Authenticate": "Bearer"},
        )
