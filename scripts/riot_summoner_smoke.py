import asyncio

from synapsecord_core.config import get_settings
from synapsecord_core.integration.riot import (
    RiotAccountAPI,
    RiotAPIClient,
    RiotPlatform,
    RiotSummonerAPI,
    region_for_platform,
)


async def main():
    settings = get_settings()

    if not settings.riot_api_key:
        raise RuntimeError("RIOT_API_KEY is not configured")

    platform = RiotPlatform(input("Platform: ").strip().lower())
    game_name = input("Game name: ").strip()
    tag_line = input("Tag line: ").strip()

    region = region_for_platform(platform)

    async with RiotAPIClient(settings.riot_api_key) as client:
        account_api = RiotAccountAPI(client)
        summoner_api = RiotSummonerAPI(client)

        account = await account_api.get_by_riot_id(region, game_name, tag_line)

        print(account)

        summoner = await summoner_api.get_by_puuid(platform, account.puuid)

        print(summoner)


if __name__ == "__main__":
    asyncio.run(main())
