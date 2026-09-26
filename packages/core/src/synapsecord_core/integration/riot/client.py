from collections.abc import Mapping
from time import perf_counter
from typing import Any

import httpx
from synapsecord_core.integration.riot.errors import (
    RiotAPIError,
    RiotAuthenticationError,
    RiotInvalidResponseError,
    RiotNotFoundError,
    RiotRateLimitError,
    RiotServiceUnavailableError,
    RiotTransportError,
)
from synapsecord_core.integration.riot.routing import (
    RiotPlatform,
    RiotRegion,
    platform_base_url,
    region_base_url,
)
from synapsecord_core.logging import get_logger

logger = get_logger(__name__)

type QueryParams = Mapping[str, str | int | float | bool | None]
type JSONPayload = dict[str, Any] | list[Any]


class RiotAPIClient:
    def __init__(
            self,
            api_key: str,
            *,
            timeout: float = 10.0,
            client: httpx.AsyncClient | None = None
    ):
        self._api_key = api_key
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)

    async def get_platform(
            self,
            platform: RiotPlatform,
            path: str,
            *,
            params: QueryParams | None = None
    ) -> JSONPayload:
        return await self._get(
            base_url=platform_base_url(platform),
            path=path,
            params=params
        )

    async def get_regional(
            self,
            region: RiotRegion,
            path: str,
            *,
            params: QueryParams | None = None
    ) -> JSONPayload:
        return await self._get(
            base_url=region_base_url(region),
            path=path,
            params=params
        )

    async def _get(
            self,
            *,
            base_url: str,
            path: str,
            params: QueryParams | None = None
    ) -> JSONPayload:
        url = f"{base_url}{path}"
        started_at = perf_counter()

        logger.debug(
            "riot_request_started",
            method="GET",
            base_url=base_url,
            path=path
        )

        try:
            response = await self._client.get(
                url,
                headers={"X-Riot-Token": self._api_key},
                params=params
            )
        except httpx.RequestError as error:
            logger.warning(
                "riot_transport_failed",
                method="GET",
                base_url=base_url,
                path=path,
                error_type=type(error).__name__
            )
            raise RiotTransportError("Failed to contact Riot API") from error

        duration_ms = round(
            (perf_counter() - started_at) * 1000,
            2
        )

        logger.debug(
            "riot_request_completed",
            method="GET",
            base_url=base_url,
            path=path,
            status_code=response.status_code,
            duration_ms=duration_ms
        )

        self._raise_for_status(response)

        try:
            payload = response.json()
        except ValueError as error:
            raise RiotInvalidResponseError(
                "Riot API returned invalid JSON response",
                status_code=response.status_code
            ) from error

        if not isinstance(payload, dict | list):
            raise RiotInvalidResponseError(
                "Riot API returned invalid JSON response",
                status_code=response.status_code
            )

        return payload

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        status_code = response.status_code

        if 200 <= status_code < 300:
            return

        if status_code in (401, 403):
            raise RiotAuthenticationError("Riot API authentication failed", status_code=status_code)

        if status_code == 404:
            raise RiotNotFoundError("Riot resource notr found", status_code=status_code)

        if status_code == 429:
            raise RiotRateLimitError(
                retry_after=RiotAPIClient._parse_retry_after(response)
            )

        if 500 <= status_code < 600:
            raise RiotServiceUnavailableError(
                "Riot API is temporarily unavailable",
                status_code=status_code
            )

        raise RiotAPIError("Riot API request failed", status_code=status_code)

    @staticmethod
    def _parse_retry_after(response: httpx.Response) -> float | None:
        value = response.headers.get("Retry-After")

        if value is None:
            return None

        try:
            return float(value)
        except ValueError:
            return None

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> RiotAPIClient:
        return self

    async def __aexit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        await self.close()
