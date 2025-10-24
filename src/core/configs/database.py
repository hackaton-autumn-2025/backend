from pydantic import PostgresDsn

from src.core.configs.base_settings import BaseSetting


class DatabaseSettings(BaseSetting):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_DB: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    DATABASE_ECHO: bool = False

    @property
    def database_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.DATABASE_USER,
                password=self.DATABASE_PASSWORD,
                host=self.DATABASE_HOST,
                port=self.DATABASE_PORT,
                path=self.DATABASE_DB,
            )
        )

    @property
    def sync_database_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.DATABASE_USER,
                password=self.DATABASE_PASSWORD,
                host=self.DATABASE_HOST,
                port=self.DATABASE_PORT,
                path=self.DATABASE_DB,
            )
        )
