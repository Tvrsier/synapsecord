import httpx
import pytest
from synapsecord_core.integration.riot import (
    RiotAPIClient,
    RiotAPIError,
    RiotAuthenticationError,
    RiotInvalidResponseError,
    RiotNotFoundError,
    RiotRateLimitError,
    RiotRegion,
    RiotServiceUnavailableError,
    RiotTransportError,
)


@pytest.mark.asyncio
async def test_get_regional_returns_json_payload() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == ("https://europe.api.riotgames.com/test")
        assert request.headers["X-Riot-Token"] == "test-key"

        return httpx.Response(200, json={"puuid": "abc"})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        payload = await client.get_regional(RiotRegion.EUROPE, "/test")

    assert payload == {"puuid": "abc"}

@pytest.mark.asyncio
async def test_get_regional_returns_json_list() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=["EUW1_1", "EUW1_2"])

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        payload = await client.get_regional(RiotRegion.EUROPE, "/test")

    assert payload == ["EUW1_1", "EUW1_2"]

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status_code", "error_type"),
    [
        (401, RiotAuthenticationError),
        (403, RiotAuthenticationError),
        (404, RiotNotFoundError),
        (500, RiotServiceUnavailableError),
        (502, RiotServiceUnavailableError),
        (503, RiotServiceUnavailableError)
    ]
)
async def test_http_status_is_mapped(status_code: int, error_type: type[RiotAPIError]) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        with pytest.raises(error_type) as captured:
            await client.get_regional(RiotRegion.EUROPE, "/test")

    assert captured.value.status_code == status_code

@pytest.mark.asyncio
async def test_rate_limit_preserves_retry_after() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, headers={"Retry-After": "12.5"})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        with pytest.raises(RiotRateLimitError) as captured:
            await client.get_regional(RiotRegion.EUROPE, "/test")

    assert captured.value.status_code == 429
    assert captured.value.retry_after == 12.5

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "retry_after",
    [
        None,
        "invalid"
    ]
)
async def test_invalid_retry_becomes_none(retry_after: str | None) -> None:
    headers = {}

    if retry_after is not None:
        headers["Retry-After"] = retry_after

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, headers=headers)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        with pytest.raises(RiotRateLimitError) as captured:
            await client.get_regional(RiotRegion.EUROPE, "/test")

    assert captured.value.retry_after is None

@pytest.mark.asyncio
async def test_invalid_json_raises_invalid_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="not-json")

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        with pytest.raises(RiotInvalidResponseError):
            await client.get_regional(RiotRegion.EUROPE, "/test")

@pytest.mark.asyncio
async def test_scalar_json_raises_invalid_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json="unexpected0")

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        with pytest.raises(RiotInvalidResponseError):
            await client.get_regional(RiotRegion.EUROPE, "/test")

@pytest.mark.asyncio
async def test_transport_error_is_wrapped() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed", request=request)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        with pytest.raises(RiotTransportError):
            await client.get_regional(RiotRegion.EUROPE, "/test")

@pytest.mark.asyncio
async def test_query_params_are_forwarded() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["count"] == "20"
        assert request.url.params["start"] == "0"

        return httpx.Response(200, json=[])

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = RiotAPIClient("test-key", client=http_client)

        await client.get_regional(RiotRegion.EUROPE, "/test", params={"count": 20, "start": 0})
