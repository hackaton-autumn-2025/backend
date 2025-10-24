from src.core.configs.base_settings import BaseSetting


class LoggingSettings(BaseSetting):
    LOG_LEVEL: str = "info"
    ACCESS_LOG: bool = True
