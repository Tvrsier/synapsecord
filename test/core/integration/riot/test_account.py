import pytest
from synapsecord_core.integration.riot import (
    RiotAccount,
    RiotAccountAPI,
    RiotInvalidResponseError,
    RiotRegion,
)


# noinspection unused-parameter
class FakeRiotAPIClient:
    def __init__(self, payload: dict[str, object] | list[object]):
        self.payload = payload
        self.region: RiotRegion | None = None
        self.path: str | None = None

    async def get_regional(
        self, region: RiotRegion, path: str, *, params=None
    ) -> dict[str, object] | list[object]:
        self.region = region
        self.path = path
        return self.payload


@pytest.mark.asyncio
async def test_get_by_riot_id() -> None:
    client = FakeRiotAPIClient(
        payload={"puuid": "test-puuid", "gameName": "Tvrsier", "tagLine": "EUW"}
    )

    api = RiotAccountAPI(client)

    account = await api.get_by_riot_id(RiotRegion.EUROPE, "Tvrsier", "EUW")

    assert account == RiotAccount(puuid="test-puuid", game_name="Tvrsier", tag_line="EUW")

    assert client.region is RiotRegion.EUROPE
    assert client.path == "/riot/account/v1/accounts/by-riot-id/Tvrsier/EUW"


@pytest.mark.asyncio
async def test_get_by_riot_id_encodes_path_values() -> None:
    client = FakeRiotAPIClient(
        {
            "puuid": "test-puuid",
            "gameName": "Some Name",
            "tagLine": "EU/W",
        }
    )
    api = RiotAccountAPI(client)  # type: ignore[arg-type]

    await api.get_by_riot_id(
        RiotRegion.EUROPE,
        "Some Name",
        "EU/W",
    )

    assert client.path == "/riot/account/v1/accounts/by-riot-id/Some%20Name/EU%2FW"


@pytest.mark.asyncio
async def test_get_by_puuid_returns_account() -> None:
    client = FakeRiotAPIClient(
        {
            "puuid": "test-puuid",
            "gameName": "Tvrsier",
            "tagLine": "EUW",
        }
    )
    api = RiotAccountAPI(client)  # type: ignore[arg-type]

    account = await api.get_by_puuid(
        RiotRegion.EUROPE,
        "test-puuid",
    )

    assert account.puuid == "test-puuid"
    assert client.path == "/riot/account/v1/accounts/by-puuid/test-puuid"


@pytest.mark.asyncio
async def test_account_rejects_non_object_payload() -> None:
    client = FakeRiotAPIClient([])
    api = RiotAccountAPI(client)  # type: ignore[arg-type]

    with pytest.raises(RiotInvalidResponseError):
        await api.get_by_riot_id(
            RiotRegion.EUROPE,
            "Tvrsier",
            "EUW",
        )

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {},
        {
            "gameName": "Tvrsier",
            "tagLine": "EUW",
        },
        {
            "puuid": None,
            "gameName": "Tvrsier",
            "tagLine": "EUW",
        },
        {
            "puuid": "abc",
            "gameName": 123,
            "tagLine": "EUW",
        },
    ],
)
async def test_account_rejects_invalid_fields(
    payload: dict[str, object],
) -> None:
    client = FakeRiotAPIClient(payload)
    api = RiotAccountAPI(client)  # type: ignore[arg-type]

    with pytest.raises(RiotInvalidResponseError):
        await api.get_by_riot_id(
            RiotRegion.EUROPE,
            "Tvrsier",
            "EUW",
        )
