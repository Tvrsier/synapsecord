from dataclasses import dataclass
from urllib.parse import quote

from synapsecord_core.integration.riot.client import RiotAPIClient
from synapsecord_core.integration.riot.errors import RiotInvalidResponseError
from synapsecord_core.integration.riot.routing import RiotPlatform
from synapsecord_core.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class RiotLeagueEntry:
    queue_type: str
    tier: str
    rank: str
    puuid: str
    league_points: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool


class RiotLeagueAPI:
    def __init__(self, client: RiotAPIClient) -> None:
        self._client = client

    async def get_entries_by_puuid(
        self,
        platform: RiotPlatform,
        puuid: str,
    ) -> list[RiotLeagueEntry]:
        encoded_puuid = quote(puuid, safe="")

        payload = await self._client.get_platform(
            platform,
            f"/lol/league/v4/entries/by-puuid/{encoded_puuid}",
        )

        return self._parse_entries(payload)

    @staticmethod
    def _parse_entries(
        payload: dict[str, object] | list[object],
    ) -> list[RiotLeagueEntry]:
        if not isinstance(payload, list):
            raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid payload")

        # noinspection unresolved-references
        logger.debug("riot_league_payload_received", count=len(payload))
        entries: list[RiotLeagueEntry] = []

        for item in payload:
            if not isinstance(item, dict):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid league entry")

            queue_type = item.get("queueType")
            tier = item.get("tier")
            rank = item.get("rank")
            puuid = item.get("puuid")
            league_points = item.get("leaguePoints")
            wins = item.get("wins")
            losses = item.get("losses")
            veteran = item.get("veteran")
            inactive = item.get("inactive")
            fresh_blood = item.get("freshBlood")
            hot_streak = item.get("hotStreak")

            if not isinstance(queue_type, str):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid queue type")

            if not isinstance(tier, str):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid tier")

            if not isinstance(rank, str):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid rank")

            if not isinstance(puuid, str):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid puuid")

            if not isinstance(league_points, int):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid league points")

            if not isinstance(wins, int):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid wins")

            if not isinstance(losses, int):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid losses")

            if not isinstance(veteran, bool):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid veteran")

            if not isinstance(inactive, bool):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid inactive")

            if not isinstance(fresh_blood, bool):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid fresh blood")

            if not isinstance(hot_streak, bool):
                raise RiotInvalidResponseError("LEAGUE-V4 returned an invalid hot streak")

            entries.append(
                RiotLeagueEntry(
                    queue_type=queue_type,
                    tier=tier,
                    rank=rank,
                    puuid=puuid,
                    league_points=league_points,
                    wins=wins,
                    losses=losses,
                    veteran=veteran,
                    inactive=inactive,
                    fresh_blood=fresh_blood,
                    hot_streak=hot_streak,
                )
            )
        return entries
