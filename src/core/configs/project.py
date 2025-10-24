from src.core.configs.base_settings import BaseSetting


class ProjectSettings(BaseSetting):
    PROJECT_NAME: str
    VERSION: str

    HOST: str = "localhost"
    PORT: int = 8080

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43_200
