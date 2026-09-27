from dataclasses import dataclass
from urllib.parse import quote

from synapsecord_core.integration.riot.client import RiotAPIClient
from synapsecord_core.integration.riot.errors import RiotInvalidResponseError
from synapsecord_core.integration.riot.routing import RiotRegion
from synapsecord_core.logging import get_logger

logger = get_logger(__name__)

@dataclass(frozen=True, slots=True)
class RiotAccount:
    puuid: str
    game_name: str
    tag_line: str


class RiotAccountAPI:
    def __init__(self, client: RiotAPIClient):
        self._client = client

    async def get_by_riot_id(
        self,
        region: RiotRegion,
        game_name: str,
        tag_line: str,
    ) -> RiotAccount:
        encoded_game_name = quote(game_name, safe="")
        encoded_tag_line = quote(tag_line, safe="")

        payload = await self._client.get_regional(
            region, f"/riot/account/v1/accounts/by-riot-id/{encoded_game_name}/{encoded_tag_line}"
        )

        return self._parse_account(payload)

    async def get_by_puuid(self, region: RiotRegion, puuid: str) -> RiotAccount:
        encoded_puuid = quote(puuid, safe="")

        payload = await self._client.get_regional(
            region, f"/riot/account/v1/accounts/by-puuid/{encoded_puuid}"
        )

        return self._parse_account(payload)

    @staticmethod
    def _parse_account(
        payload: dict[str, object] | list[object],
    ) -> RiotAccount:
        if not isinstance(payload, dict):
            raise RiotInvalidResponseError("ACCOUNT-V1 returned an invalid payload")

        logger.debug(
            "riot_account_payload_received",
            fields=sorted(payload.keys()),
        )

        puuid = payload.get("puuid")
        game_name = payload.get("gameName")
        tag_line = payload.get("tagLine")

        if not all(isinstance(value, str) for value in (puuid, game_name, tag_line)):
            raise RiotInvalidResponseError("ACCOUNT-V1 returned an invalid account payload")

        return RiotAccount(puuid, game_name, tag_line)
