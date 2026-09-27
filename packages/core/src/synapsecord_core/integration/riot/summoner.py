from dataclasses import dataclass
from urllib.parse import quote

from synapsecord_core.integration.riot import RiotPlatform
from synapsecord_core.integration.riot.client import RiotAPIClient
from synapsecord_core.integration.riot.errors import RiotInvalidResponseError
from synapsecord_core.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class RiotSummoner:
    puuid: str
    profile_icon_id: int
    revision_date: int
    summoner_level: int


class RiotSummonerAPI:
    def __init__(self, client: RiotAPIClient):
        self._client = client

    async def get_by_puuid(self, platform: RiotPlatform, puuid: str) -> RiotSummoner:
        encoded_puuid = quote(puuid, safe="")

        payload = await self._client.get_platform(
            platform, f"/lol/summoner/v4/summoners/by-puuid/{encoded_puuid}"
        )

        return self._parse_summoner(payload)

    @staticmethod
    def _parse_summoner(payload: dict[str, object] | list[object]) -> RiotSummoner:
        if not isinstance(payload, dict):
            raise RiotInvalidResponseError("SUMMONER-V4 returned an invalid payload")

        logger.debug(
            "riot_summoner_payload_received",
            fields=sorted(payload.keys()),
        )

        puuid = payload.get("puuid")
        profile_icon_id = payload.get("profileIconId")
        revision_date = payload.get("revisionDate")
        summoner_level = payload.get("summonerLevel")

        if not isinstance(puuid, str):
            raise RiotInvalidResponseError("SUMMONER-V4 returned an invalid PUUID")

        if not isinstance(profile_icon_id, int):
            raise RiotInvalidResponseError("SUMMONER-V4 returned an invalid profile icon id")

        if not isinstance(revision_date, int):
            raise RiotInvalidResponseError("SUMMONER-V4 returned an invalid revision date")

        if not isinstance(summoner_level, int):
            raise RiotInvalidResponseError("SUMMONER-V4 returned an invalid summoner level")

        return RiotSummoner(
            puuid=puuid,
            profile_icon_id=profile_icon_id,
            revision_date=revision_date,
            summoner_level=summoner_level,
        )
