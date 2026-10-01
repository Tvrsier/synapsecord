from synapsecord_core.config import get_settings
from synapsecord_core.integration.riot import (
    RiotAccountAPI,
    RiotAPIClient,
    RiotMatchAPI,
    RiotPlatform,
    region_for_platform,
)


async def main():
    settings = get_settings()

    if not settings.riot_api_key:
        raise RuntimeError("RIOT_API_KEY is not configured")
    platform = RiotPlatform(input("Platform: ").strip().lower())
    region = region_for_platform(platform)

    game_name = input("Game name: ")
    tag_line = input("Tag line: ")

    async with RiotAPIClient(settings.riot_api_key) as client:
        account_api = RiotAccountAPI(client)

        account = await account_api.get_by_riot_id(region, game_name, tag_line)

        match_api = RiotMatchAPI(client)

        match_ids_1 = await match_api.get_match_ids(
            region, account.puuid, queue=420, match_type="ranked", count=5
        )
        match_ids_2 = await match_api.get_match_ids(
            region, account.puuid, queue=420, match_type="ranked", count=5, start=5
        )

    print(match_ids_1)
    print(match_ids_2)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
