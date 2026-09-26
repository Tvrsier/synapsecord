from enum import StrEnum


class RiotPlatform(StrEnum):
    BR1 = "br1"
    EUN1 = "eun1"
    EUW1 = "euw1"
    JP1 = "jp1"
    KR = "kr"
    LA1 = "la1"
    LA2 = "la2"
    NA1 = "na1"
    OC1 = "oc1"
    TR1 = "tr1"
    RU = "ru"
    PH2 = "ph2"
    SG2 = "sg2"
    TH2 = "th2"
    TW2 = "tw2"
    VN2 = "vn2"


class RiotRegion(StrEnum):
    EUROPE = "europe"
    AMERICAS = "americas"
    ASIA = "asia"
    SEA = "sea"


_PLATFORM_TO_REGION: dict[RiotPlatform, RiotRegion] = {
    RiotPlatform.BR1: RiotRegion.AMERICAS,
    RiotPlatform.NA1: RiotRegion.AMERICAS,
    RiotPlatform.LA1: RiotRegion.AMERICAS,
    RiotPlatform.LA2: RiotRegion.AMERICAS,
    RiotPlatform.OC1: RiotRegion.AMERICAS,

    RiotPlatform.EUW1: RiotRegion.EUROPE,
    RiotPlatform.EUN1: RiotRegion.EUROPE,
    RiotPlatform.TR1: RiotRegion.EUROPE,
    RiotPlatform.RU: RiotRegion.EUROPE,

    RiotPlatform.JP1: RiotRegion.ASIA,
    RiotPlatform.KR: RiotRegion.ASIA,

    RiotPlatform.PH2: RiotRegion.SEA,
    RiotPlatform.SG2: RiotRegion.SEA,
    RiotPlatform.TH2: RiotRegion.SEA,
    RiotPlatform.TW2: RiotRegion.SEA,
    RiotPlatform.VN2: RiotRegion.SEA,
}

def region_for_platform(platform: RiotPlatform) -> RiotRegion:
    return _PLATFORM_TO_REGION[platform]

def platform_base_url(platform: RiotPlatform) -> str:
    return f"https://{platform.value}.api.riotgames.com"

def region_base_url(region: RiotRegion) -> str:
    return f"https://{region.value}.api.riotgames.com"