import pytest
from synapsecord_core.integration.riot import (
    RiotInvalidResponseError,
    RiotLeagueAPI,
    RiotLeagueEntry,
    RiotPlatform,
)

VALID_ENTRY: dict[str, object] = {
    "queueType": "RANKED_SOLO_5x5",
    "tier": "PLATINUM",
    "rank": "II",
    "puuid": "test-puuid",
    "leaguePoints": 12,
    "wins": 249,
    "losses": 256,
    "veteran": False,
    "inactive": False,
    "freshBlood": False,
    "hotStreak": False,
}


class FakeRiotAPIClient:
    def __init__(
        self,
        payload: dict[str, object] | list[object],
    ) -> None:
        self.payload = payload
        self.platform: RiotPlatform | None = None
        self.path: str | None = None

    # noinspection unused-parameter
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
async def test_get_entries_by_puuid_returns_entries() -> None:
    client = FakeRiotAPIClient(
        [
            {
                "queueType": "RANKED_SOLO_5x5",
                "tier": "PLATINUM",
                "rank": "II",
                "puuid": "test-puuid",
                "leaguePoints": 12,
                "wins": 249,
                "losses": 256,
                "veteran": False,
                "inactive": False,
                "freshBlood": False,
                "hotStreak": False,
            },
            {
                "queueType": "RANKED_FLEX_SR",
                "tier": "GOLD",
                "rank": "I",
                "puuid": "test-puuid",
                "leaguePoints": 1,
                "wins": 27,
                "losses": 17,
                "veteran": False,
                "inactive": False,
                "freshBlood": False,
                "hotStreak": True,
            },
        ]
    )

    api = RiotLeagueAPI(client)

    entries = await api.get_entries_by_puuid(
        RiotPlatform.EUW1,
        "test-puuid",
    )

    assert entries == [
        RiotLeagueEntry(
            queue_type="RANKED_SOLO_5x5",
            tier="PLATINUM",
            rank="II",
            puuid="test-puuid",
            league_points=12,
            wins=249,
            losses=256,
            veteran=False,
            inactive=False,
            fresh_blood=False,
            hot_streak=False,
        ),
        RiotLeagueEntry(
            queue_type="RANKED_FLEX_SR",
            tier="GOLD",
            rank="I",
            puuid="test-puuid",
            league_points=1,
            wins=27,
            losses=17,
            veteran=False,
            inactive=False,
            fresh_blood=False,
            hot_streak=True,
        ),
    ]

    assert client.platform is RiotPlatform.EUW1
    assert client.path == "/lol/league/v4/entries/by-puuid/test-puuid"


@pytest.mark.asyncio
async def test_empty_entries_are_valid() -> None:
    client = FakeRiotAPIClient([])
    api = RiotLeagueAPI(client)

    entries = await api.get_entries_by_puuid(
        RiotPlatform.EUW1,
        "test-puuid",
    )

    assert entries == []


@pytest.mark.asyncio
async def test_get_entries_by_puuid_encodes_path_value() -> None:
    client = FakeRiotAPIClient([])
    api = RiotLeagueAPI(client)

    await api.get_entries_by_puuid(
        RiotPlatform.EUW1,
        "test/value",
    )

    assert client.path == "/lol/league/v4/entries/by-puuid/test%2Fvalue"


@pytest.mark.asyncio
async def test_rejects_non_list_payload() -> None:
    client = FakeRiotAPIClient(
        {
            "queueType": "RANKED_SOLO_5x5",
        }
    )
    api = RiotLeagueAPI(client)

    with pytest.raises(RiotInvalidResponseError):
        await api.get_entries_by_puuid(
            RiotPlatform.EUW1,
            "test-puuid",
        )


@pytest.mark.asyncio
async def test_rejects_non_object_entry() -> None:
    client = FakeRiotAPIClient(
        [
            "invalid-entry",
        ]
    )
    api = RiotLeagueAPI(client)

    with pytest.raises(RiotInvalidResponseError):
        await api.get_entries_by_puuid(
            RiotPlatform.EUW1,
            "test-puuid",
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("queueType", None),
        ("tier", None),
        ("rank", None),
        ("puuid", None),
        ("leaguePoints", "12"),
        ("wins", "249"),
        ("losses", "256"),
        ("veteran", 0),
        ("inactive", 0),
        ("freshBlood", 0),
        ("hotStreak", 0),
    ],
)
async def test_rejects_invalid_entry_fields(
    field: str,
    value: object,
) -> None:
    entry = VALID_ENTRY.copy()
    entry[field] = value

    client = FakeRiotAPIClient([entry])
    api = RiotLeagueAPI(client)

    with pytest.raises(RiotInvalidResponseError):
        await api.get_entries_by_puuid(
            RiotPlatform.EUW1,
            "test-puuid",
        )
