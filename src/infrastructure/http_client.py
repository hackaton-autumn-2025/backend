from dataclasses import dataclass
from typing import Any

import httpx

from src.core.log import logger
from src.enums.http import HttpMethod


class HttpClientError(Exception):
    pass


class HttpRequestError(HttpClientError):
    pass

class HttpResponseError(HttpClientError):
    pass


@dataclass
class HttpClient:

    @staticmethod
    async def _request(
        method: HttpMethod,
        url: httpx.URL,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 5,
    ) -> dict[str, Any]:
        merged_headers = {"Accept": "application/json"}
        if headers:
            merged_headers.update(headers)

        async with httpx.AsyncClient(timeout=timeout, headers=merged_headers) as client:
            try:
                print("ФЫФЫВ")
                print(url, method, params, json)
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                )
                logger.info(
                    "✅ HTTP response received",
                    extra={
                        "status_code": response.status_code,
                        "url": str(response.url),
                        "response_text": (
                            response.text[:500] + "..." if len(response.text) > 500 else response.text
                        )
                    }
                )
                response.raise_for_status()
            except httpx.RequestError as exc:
                raise HttpRequestError(f"Ошибка при соединении: {exc}") from exc
            except httpx.HTTPStatusError as exc:
                raise HttpResponseError(f"HTTP {exc.response.status_code}: {exc.response.text}") from exc

            return response.json()


    @staticmethod
    async def get(
        url: httpx.URL,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 5,
    ):
        return await HttpClient._request(HttpMethod.GET.value, url, params=params, headers=headers, timeout=timeout)

    @staticmethod
    async def post(
        url: httpx.URL,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 5,
    ):
        return await HttpClient._request(HttpMethod.POST.value, url, json=json, headers=headers, timeout=timeout)

    @staticmethod
    async def put(
        url: httpx.URL,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 5,
    ):
        return await HttpClient._request(HttpMethod.PUT.value, url, json=json, headers=headers, timeout=timeout)

    @staticmethod
    async def delete(
        url: httpx.URL,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 5,
    ):
        return await HttpClient._request(HttpMethod.DELETE.value, url, params=params, headers=headers, timeout=timeout)
