import pytest
from synapsecord_core.integration.riot import (
    RiotInvalidResponseError,
    RiotPlatform,
    RiotSummoner,
    RiotSummonerAPI,
)


class FakeRiotAPIClient:
    def __init__(
        self,
        payload: dict[str, object] | list[object],
    ) -> None:
        self.payload = payload
        self.platform: RiotPlatform | None = None
        self.path: str | None = None

    async def get_platform(
        self,
        platform: RiotPlatform,
        path: str,
        *,
        params=None,
    ):
        self.platform = platform
        self.path = path
        return self.payload


@pytest.mark.asyncio
async def test_get_by_puuid_returns_summoner() -> None:
    client = FakeRiotAPIClient(
        {
            "puuid": "test-puuid",
            "profileIconId": 1234,
            "revisionDate": 1700000000000,
            "summonerLevel": 500,
        }
    )

    api = RiotSummonerAPI(client)

    summoner = await api.get_by_puuid(
        RiotPlatform.EUW1,
        "test-puuid",
    )

    assert summoner == RiotSummoner(
        puuid="test-puuid",
        profile_icon_id=1234,
        revision_date=1700000000000,
        summoner_level=500,
    )

    assert client.platform is RiotPlatform.EUW1
    assert client.path == "/lol/summoner/v4/summoners/by-puuid/test-puuid"


@pytest.mark.asyncio
async def test_get_by_puuid_encodes_path_value() -> None:
    client = FakeRiotAPIClient(
        {
            "puuid": "test/value",
            "profileIconId": 1234,
            "revisionDate": 1700000000000,
            "summonerLevel": 500,
        }
    )

    api = RiotSummonerAPI(client)

    await api.get_by_puuid(
        RiotPlatform.EUW1,
        "test/value",
    )

    assert client.path == "/lol/summoner/v4/summoners/by-puuid/test%2Fvalue"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        {
            "puuid": None,
            "profileIconId": 1234,
            "revisionDate": 1700000000000,
            "summonerLevel": 500,
        },
        {
            "id": "summoner-id",
            "puuid": "test-puuid",
            "profileIconId": "1234",
            "revisionDate": 1700000000000,
            "summonerLevel": 500,
        },
    ],
)
async def test_rejects_invalid_payload(
    payload: dict[str, object] | list[object],
) -> None:
    client = FakeRiotAPIClient(payload)
    api = RiotSummonerAPI(client)

    with pytest.raises(RiotInvalidResponseError):
        await api.get_by_puuid(
            RiotPlatform.EUW1,
            "test-puuid",
        )
