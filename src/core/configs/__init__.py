from src.core.configs.database import DatabaseSettings
from src.core.configs.http import InfrastructureSettings
from src.core.configs.log import LoggingSettings
from src.core.configs.project import ProjectSettings


class Settings:
    db_settings = DatabaseSettings()
    project_settings = ProjectSettings()
    log_settings = LoggingSettings()
    infra_settings = InfrastructureSettings()


settings = Settings()
