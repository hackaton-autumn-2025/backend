from enum import StrEnum, unique


@unique
class TokenType(StrEnum):
    REFRESH = "REFRESH"
    ACCESS = "ACCESS"
