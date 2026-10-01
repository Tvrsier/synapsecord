from urllib.parse import quote

from synapsecord_core.integration.riot.client import RiotAPIClient
from synapsecord_core.integration.riot.errors import RiotInvalidResponseError
from synapsecord_core.integration.riot.routing import RiotRegion


class RiotMatchAPI:
    def __init__(self, client: RiotAPIClient):
        self._client = client

    async def get_match_ids(
        self,
        region: RiotRegion,
        puuid: str,
        *,
        start: int = 0,
        count: int = 20,
        start_time: int | None = None,
        end_time: int | None = None,
        queue: int | None = None,
        match_type: str | None = None,
    ) -> list[str]:
        encoded_puuid = quote(puuid, safe="")

        params: dict[str, str | int] = {"start": start, "count": count}

        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time

        if queue is not None:
            params["queue"] = queue

        if match_type is not None:
            params["type"] = match_type

        payload = await self._client.get_regional(
            region, f"/lol/match/v5/matches/by-puuid/{encoded_puuid}/ids", params=params
        )

        return self._parse_match_ids(payload)

    @staticmethod
    def _parse_match_ids(payload: dict[str, object] | list[object]) -> list[str]:
        if not isinstance(payload, list):
            raise RiotInvalidResponseError("MATCH-V5 returned an invalid match payload")

        if not all(isinstance(match_id, str) for match_id in payload):
            raise RiotInvalidResponseError("MATCH-V5 returned an invalid match payload")

        return payload
