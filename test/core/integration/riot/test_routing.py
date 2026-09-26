import pytest
from synapsecord_core.integration.riot import (
    RiotPlatform,
    RiotRegion,
    platform_base_url,
    region_base_url,
    region_for_platform,
)


def test_platform_base_url():
    for platform in RiotPlatform:
        assert platform_base_url(platform) == f"https://{platform.value}.api.riotgames.com"

def test_region_base_url():
    for region in RiotRegion:
        assert region_base_url(region) == f"https://{region.value}.api.riotgames.com"

@pytest.mark.parametrize(
    ("platform", "region"),
    [
        (RiotPlatform.BR1, RiotRegion.AMERICAS),
        (RiotPlatform.NA1, RiotRegion.AMERICAS),
        (RiotPlatform.LA1, RiotRegion.AMERICAS),
        (RiotPlatform.LA2, RiotRegion.AMERICAS),
        (RiotPlatform.OC1, RiotRegion.AMERICAS),

        (RiotPlatform.EUW1, RiotRegion.EUROPE),
        (RiotPlatform.EUN1, RiotRegion.EUROPE),
        (RiotPlatform.TR1, RiotRegion.EUROPE),
        (RiotPlatform.RU, RiotRegion.EUROPE),

        (RiotPlatform.JP1, RiotRegion.ASIA),
        (RiotPlatform.KR, RiotRegion.ASIA),

        (RiotPlatform.PH2, RiotRegion.SEA),
        (RiotPlatform.SG2, RiotRegion.SEA),
        (RiotPlatform.TH2, RiotRegion.SEA),
        (RiotPlatform.TW2, RiotRegion.SEA),
        (RiotPlatform.VN2, RiotRegion.SEA),
    ],
)
def test_region_for_platform(
    platform: RiotPlatform,
    region: RiotRegion,
) -> None:
    assert region_for_platform(platform) is region