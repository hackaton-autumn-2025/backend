from enum import StrEnum, unique


@unique
class HttpMethod(StrEnum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"