from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.core.configs import settings
from src.infrastructure.database.base import Base


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.async_session_factory = None
        self._initialized = False

    def init(self):
        if self._initialized:
            return

        self.engine = create_async_engine(
            settings.db_settings.database_url,
            echo=settings.db_settings.DATABASE_ECHO,
            poolclass=NullPool,
            future=True,
        )

        self.async_session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        self._initialized = True

    async def create_tables(self):
        if not self._initialized:
            raise RuntimeError("Database manager not initialized. Call init() first.")

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[Any, Any]:
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self):
        if self.engine:
            await self.engine.dispose()


db_manager = DatabaseManager()
