import pytest
from synapsecord_core.integration.riot import RiotInvalidResponseError, RiotMatchAPI, RiotRegion


class FakeRiotAPIClient:
    def __init__(
        self,
        payload: dict[str, object] | list[object],
    ) -> None:
        self.payload = payload
        self.region: RiotRegion | None = None
        self.path: str | None = None
        self.params = None

    async def get_regional(
        self,
        region: RiotRegion,
        path: str,
        *,
        params=None,
    ):
        self.region = region
        self.path = path
        self.params = params
        return self.payload


@pytest.mark.asyncio
async def test_get_match_ids_by_puuid_returns_ids() -> None:
    client = FakeRiotAPIClient(
        [
            "EUW1_100",
            "EUW1_99",
        ]
    )
    api = RiotMatchAPI(client)

    match_ids = await api.get_match_ids(
        RiotRegion.EUROPE,
        "test-puuid",
    )

    assert match_ids == [
        "EUW1_100",
        "EUW1_99",
    ]

    assert client.region is RiotRegion.EUROPE
    assert client.path == ("/lol/match/v5/matches/by-puuid/test-puuid/ids")
    assert client.params == {
        "start": 0,
        "count": 20,
    }


@pytest.mark.asyncio
async def test_empty_match_history_is_valid() -> None:
    client = FakeRiotAPIClient([])
    api = RiotMatchAPI(client)

    match_ids = await api.get_match_ids(
        RiotRegion.EUROPE,
        "test-puuid",
    )

    assert match_ids == []


@pytest.mark.asyncio
async def test_start_and_count_are_forwarded() -> None:
    client = FakeRiotAPIClient([])
    api = RiotMatchAPI(client)

    await api.get_match_ids(
        RiotRegion.EUROPE,
        "test-puuid",
        start=10,
        count=5,
    )

    assert client.params == {
        "start": 10,
        "count": 5,
    }


@pytest.mark.asyncio
async def test_get_match_ids_encodes_puuid() -> None:
    client = FakeRiotAPIClient([])
    api = RiotMatchAPI(client)

    await api.get_match_ids(
        RiotRegion.EUROPE,
        "test/value",
    )

    assert client.path == "/lol/match/v5/matches/by-puuid/test%2Fvalue/ids"


@pytest.mark.asyncio
async def test_rejects_non_list_payload() -> None:
    client = FakeRiotAPIClient(
        {
            "matchId": "EUW1_100",
        }
    )
    api = RiotMatchAPI(client)

    with pytest.raises(RiotInvalidResponseError):
        await api.get_match_ids(
            RiotRegion.EUROPE,
            "test-puuid",
        )


@pytest.mark.asyncio
async def test_rejects_non_string_match_id() -> None:
    client = FakeRiotAPIClient(
        [
            "EUW1_100",
            123,
        ]
    )
    api = RiotMatchAPI(client)

    with pytest.raises(RiotInvalidResponseError):
        await api.get_match_ids(
            RiotRegion.EUROPE,
            "test-puuid",
        )


@pytest.mark.asyncio
async def test_match_filters_are_forwarded() -> None:
    client = FakeRiotAPIClient([])
    api = RiotMatchAPI(client)

    await api.get_match_ids(
        RiotRegion.EUROPE,
        "test-puuid",
        start=10,
        count=5,
        start_time=1_700_000_000,
        end_time=1_710_000_000,
        queue=420,
        match_type="ranked",
    )

    assert client.params == {
        "start": 10,
        "count": 5,
        "startTime": 1_700_000_000,
        "endTime": 1_710_000_000,
        "queue": 420,
        "type": "ranked",
    }
