from enum import StrEnum, unique


@unique
class ClientLevel(StrEnum):
    VIP = "VIP"
    CLASSIC = "CLASSIC"

@unique
class TransportMode(StrEnum):
    CAR = "CAR"
    WALK = "WALK"
