from fastapi import HTTPException


class HttpClientError(HTTPException):
    pass


class HttpRequestError(HttpClientError):
    pass


class HttpResponseError(HttpClientError):
    pass
