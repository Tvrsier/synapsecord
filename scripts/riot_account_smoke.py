import asyncio

from synapsecord_core.config import get_settings
from synapsecord_core.integration.riot import (
    RiotAccountAPI,
    RiotAPIClient,
    RiotPlatform,
    region_for_platform,
)


async def main() -> None:
    settings = get_settings()

    print("has key:", bool(settings.riot_api_key))
    print("length:", len(settings.riot_api_key) if settings.riot_api_key else None)
    print(
        "prefix:",
        settings.riot_api_key[:5] if settings.riot_api_key else None,
    )

    if not settings.riot_api_key:
        raise RuntimeError("RIOT_API_KEY is not configured")

    platform = RiotPlatform(input("Platform: ").strip().lower())
    region = region_for_platform(platform)

    game_name = input("Game name: ")
    tag_line = input("Tag line: ")

    async with RiotAPIClient(settings.riot_api_key) as client:
        account_api = RiotAccountAPI(client)

        account = await account_api.get_by_riot_id(region, game_name, tag_line)

        print(account)


if __name__ == "__main__":
    asyncio.run(main())
