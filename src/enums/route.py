from enum import StrEnum, unique


@unique
class ClientLevel(StrEnum):
    VIP = "VIP"
    STANDART = "STANDART"

@unique
class TransportMode(StrEnum):
    CAR = "CAR"
    WALK = "WALK"
