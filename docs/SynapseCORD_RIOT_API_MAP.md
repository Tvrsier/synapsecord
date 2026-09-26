# SynapseCORD — Riot API Map

_Last reviewed: 2026-09-24_

## Purpose

This document is the working API map for **M1 — Riot Integration** and the first input to **M3 — League Feature Extractor**.

The goal is to separate:

```text
Riot API
→ League API client
→ LeagueDataProvider
→ normalized SynapseCORD models
→ profiler / feature extractor
```

The Riot-specific layer must not leak raw Riot DTOs into the profiler or Discord bot.

---

## Architectural decisions already supported by Riot documentation

### Player identity

For League of Legends, SynapseCORD should use:

```text
game_accounts.external_id = PUUID
```

Riot recommends using **PUUID** when an endpoint supports it. Player-facing lookup should use **Riot ID** (`gameName + tagLine`) rather than Summoner Name.

Treat these differently:

```text
PUUID
= stable external identity used by SynapseCORD

Riot ID
= player-facing identifier; can change

summonerID
= League shard-specific identifier; use only where an API still requires it

summonerName
= deprecated / stale for player-facing identity
```

### Region is still required at onboarding

Riot's FAQ states that League player data remains sharded by League/TFT region and, as of the referenced documentation, Riot does not provide a generally available League active-shard lookup that lets us infer the League platform from Riot ID alone.

Initial account-link input should therefore conceptually be:

```text
Riot ID:
  gameName
  tagLine

League platform:
  EUW1 / EUN1 / NA1 / ...
```

This can change later if Riot exposes a reliable League active-shard API.

---

# Routing model

Riot League APIs use two routing families.

## Platform routing

Typical hosts:

```text
BR1  → br1.api.riotgames.com
EUN1 → eun1.api.riotgames.com
EUW1 → euw1.api.riotgames.com
JP1  → jp1.api.riotgames.com
KR   → kr.api.riotgames.com
LA1  → la1.api.riotgames.com
LA2  → la2.api.riotgames.com
NA1  → na1.api.riotgames.com
OC1  → oc1.api.riotgames.com
TR1  → tr1.api.riotgames.com
RU   → ru.api.riotgames.com
PH2  → ph2.api.riotgames.com
SG2  → sg2.api.riotgames.com
TH2  → th2.api.riotgames.com
TW2  → tw2.api.riotgames.com
VN2  → vn2.api.riotgames.com
```

Used primarily for League-shard-specific services such as Summoner, League and Champion Mastery.

## Regional routing

```text
AMERICAS → americas.api.riotgames.com
ASIA     → asia.api.riotgames.com
EUROPE   → europe.api.riotgames.com
SEA      → sea.api.riotgames.com
```

Used by services clustered regionally, notably ACCOUNT-V1 and MATCH-V5.

## Required SynapseCORD abstraction

Do not pass raw routing strings around unrelated code.

Conceptually:

```text
LeaguePlatform
  EUW1
  EUN1
  NA1
  ...

LeagueRegion
  EUROPE
  AMERICAS
  ASIA
  SEA
```

with an explicit mapping:

```text
LeaguePlatform → LeagueRegion
```

Example:

```text
EUW1 → EUROPE
NA1  → AMERICAS
KR   → ASIA
```

The exact mapping table should be centralized and tested.

---

# Endpoint map

## 1. ACCOUNT-V1 — Riot ID → PUUID

### Endpoint

```http
GET /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}
```

### Routing

```text
REGIONAL
```

Example host for an EU account:

```text
https://europe.api.riotgames.com
```

### Input

```text
gameName
tagLine
```

### Important output

Conceptually:

```text
puuid
gameName
tagLine
```

### SynapseCORD use

This is the first request during account linking.

```text
Riot ID
→ Account DTO
→ PUUID
```

The resulting `puuid` becomes:

```text
game_accounts.external_id
```

### Store / normalize

Likely normalized data:

```text
puuid
riot_game_name
riot_tag_line
platform
```

`gameName` and `tagLine` should be refreshable metadata rather than identity.

### Empirical validation

Test:

- Unicode/special characters in Riot IDs
- URL escaping
- wrong gameName
- wrong tagLine
- valid Riot ID on the wrong regional routing host
- current error payloads/statuses
- whether Account data is identical when queried from different valid clusters as documented

---

## 2. ACCOUNT-V1 — PUUID → current Riot ID

### Endpoint

```http
GET /riot/account/v1/accounts/by-puuid/{puuid}
```

### Routing

```text
REGIONAL
```

### Input

```text
PUUID
```

### Output

```text
puuid
gameName
tagLine
```

### SynapseCORD use

Use this to refresh mutable player-facing Riot ID data without changing identity.

Potential periodic process:

```text
stored PUUID
→ current Riot ID
→ update display metadata if changed
```

This is useful because Riot ID can change while PUUID remains the external identity.

---

# 3. SUMMONER-V4 — PUUID → League summoner data

### Endpoint

```http
GET /lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}
```

### Routing

```text
PLATFORM
```

Example:

```text
EUW1 → euw1.api.riotgames.com
```

### Input

```text
PUUID
platform
```

### Relevant output

Riot documents this endpoint as returning League summoner data and the League-specific `summonerID`.

Fields must be verified against a live payload before defining permanent DTOs.

Likely useful categories:

```text
summonerID
profile icon
summoner level
account / revision metadata where still present
```

### SynapseCORD use

This endpoint is **supporting data**, not identity.

Use it when:

- another League API still requires `summonerID`
- profile level/icon are useful for display/context
- validating that a PUUID belongs to a League account on the selected platform

### Important rule

Do not replace PUUID with summonerID as `external_id`.

---

# 4. MATCH-V5 — PUUID → match IDs

### Endpoint

```http
GET /lol/match/v5/matches/by-puuid/{puuid}/ids
```

### Routing

```text
REGIONAL
```

### Input

Required:

```text
PUUID
```

Optional filters exposed by MATCH-V5 should be validated against the live reference before implementation. Typical Match-V5 filters include concepts such as:

```text
start
count
startTime
endTime
queue
type
```

Do not hard-code these until checked against the current API reference.

### Output

```text
list[match_id]
```

Example conceptual value:

```text
EUW1_1234567890
```

### SynapseCORD use

This defines the history window for profiling and observations.

Potential use:

```text
full profile
→ larger historical sample

drift observation
→ recent bounded sample
```

### Decisions not made yet

We still need empirical data before selecting:

```text
number of matches
time window
queue filters
minimum sample size
```

Do not bake those decisions into the API client.

The provider should expose retrieval capability; profiling policy decides the desired sample.

### Empirical validation

Test:

- 0 matches
- small history
- count boundaries
- timestamp boundaries
- queue filtering
- ranked vs normal history
- remakes / early terminated games
- non-Summoner's-Rift game modes
- ordering guarantees in practice

---

# 5. MATCH-V5 — Match detail

### Endpoint

```http
GET /lol/match/v5/matches/{matchId}
```

### Routing

```text
REGIONAL
```

### Input

```text
matchId
```

### Output

`MatchDto`, conceptually split into:

```text
metadata
info
```

The participant objects are expected to contain the majority of data relevant to SynapseCORD's observed profile.

### Potentially useful feature families

Do not treat this list as a finalized feature model.

#### Identity / context

```text
PUUID
team
champion
position / role
queue
game mode
game duration
patch / game version
```

#### Combat

```text
kills
deaths
assists
damage dealt
damage taken
damage to champions
damage composition
CC-related statistics
```

#### Economy

```text
gold earned
gold spent
CS
neutral minions
items
```

#### Map / objective contribution

```text
vision
wards
objectives
turrets
team objective outcomes
```

#### Participation / behavioral context

```text
kill participation inputs
teamfight-related values
challenges fields
role / lane information
```

### Why this endpoint needs real payload research

The documented DTO is enough to implement transport and raw parsing, but **not enough to decide the final profiling vector**.

We need to inspect actual payloads to understand:

- fields consistently populated across supported queues
- fields omitted when zero/empty
- `challenges` stability and semantics
- differences by patch
- position reliability
- remakes
- mode-specific fields
- whether some values are redundant or derived
- which statistics remain useful after normalization by champion/role/rank/game duration

### Normalization principle

M3 should not consume Riot `MatchDto` directly.

Desired boundary:

```text
Riot MatchDto
→ League normalizer
→ NormalizedMatch
→ League feature extractor
```

---

# 6. MATCH-V5 — Timeline

### Endpoint

```http
GET /lol/match/v5/matches/{matchId}/timeline
```

### Routing

```text
REGIONAL
```

### Input

```text
matchId
```

### Output

A chronological match timeline containing frames/events.

Exact DTO shape must be captured from the current reference and validated using real matches.

### Potential SynapseCORD value

The timeline may enable features that final match totals cannot describe well.

Candidate concepts:

```text
early aggression
early deaths / kills
lane pressure proxies
roaming timing
objective timing
fight timing
resource acquisition over time
position/pathing proxies
recall / purchase timing
vision timing
team grouping
```

### Critical design decision

Do **not** automatically fetch timeline data for every historical match until we know its value.

Timeline approximately doubles MATCH-V5 request volume:

```text
N matches
→ N match-detail requests
→ potentially N timeline requests
```

First determine which profiler features genuinely require timeline data.

Potential strategy:

```text
match details for full sample
+
timelines only for a bounded subset
```

or:

```text
timeline extraction only for features that justify the request cost
```

### Empirical validation

We need multiple real timelines to determine:

- event types
- frame frequency
- position data availability
- participant mapping
- event consistency
- queue/mode differences
- patch differences
- practical payload size
- derived features worth retaining

---

# 7. LEAGUE-V4 — Ranked information

### Primary candidate endpoint

Current Riot API reference exposes League-v4 and PUUID-based player lookups. Confirm the exact current route in the API Reference immediately before implementation.

Expected route family:

```http
GET /lol/league/v4/entries/by-puuid/{encryptedPUUID}
```

### Routing

```text
PLATFORM
```

### Input

```text
PUUID
platform
```

### Expected useful output

Per ranked queue:

```text
queue type
tier
rank / division
league points
wins
losses
hot streak / veteran / fresh blood metadata where provided
```

### SynapseCORD use

Rank is **context**, not the player's behavioral profile itself.

Potential uses:

```text
profile normalization
matchmaking constraints
rank compatibility
sample interpretation
```

Important:

```text
RankCompatibility != PlaystyleCompatibility
```

Do not let rank dominate behavioral profiling.

### Empirical validation

Test:

- unranked account
- Solo/Duo only
- Flex only
- both queues
- newly placed account
- high-tier representation differences if any

---

# 8. CHAMPION-MASTERY-V4 — Champion mastery

### Primary endpoint

```http
GET /lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}
```

### Routing

```text
PLATFORM
```

### Input

```text
PUUID
platform
```

### Useful output categories

```text
championId
championLevel
championPoints
lastPlayTime
progression-related fields
```

Exact current DTO fields should be taken from the API reference when implementing.

### SynapseCORD use

Useful as supporting evidence for:

```text
champion pool
champion familiarity
specialization
breadth / diversity
comfort picks
```

However, mastery must not be confused with recent actual play.

Example:

```text
high historical mastery
≠
currently active champion
```

Therefore combine mastery with recent MATCH-V5 history.

### Candidate normalized concepts

```text
historical champion affinity
recent champion frequency
pool concentration
pool breadth
role-aligned champion pool
```

---

# 9. Data Dragon — Static League data

Data Dragon is not part of the authenticated gameplay API, but it is important for interpreting IDs and displaying data.

Potential use:

```text
championId → champion metadata
itemId → item metadata
runes
summoner spells
assets/icons
```

### Important Riot note

Data Dragon updates are a manual process and may not always be immediately synchronized with a League patch.

### SynapseCORD design

Static-data access should be isolated from player-data transport.

Conceptually:

```text
LeagueStaticDataProvider
```

or a small cache/service behind the League adapter.

Do not hardcode champion names against numeric IDs.

---

# Suggested M1 API boundary

Do not expose one method for every Riot HTTP endpoint to the rest of the system.

First implementation can contain a Riot-specific transport client:

```text
RiotApiClient
```

responsible for:

```text
HTTP
API key
routing
timeouts
status codes
Retry-After
rate-limit headers
JSON decoding
transport errors
```

and a higher-level:

```text
LeagueDataProvider
```

responsible for:

```text
Riot ID → account identity
League player context
match history
normalized matches
rank context
champion mastery context
```

Conceptual API only — not finalized:

```python
class LeagueDataProvider:
    def resolve_account(...)
    def get_player_context(...)
    def get_match_ids(...)
    def get_match(...)
    def get_match_timeline(...)
    def get_ranked_entries(...)
    def get_champion_masteries(...)
```

The exact async/sync choice must be made deliberately. SynapseCORD's SQLAlchemy persistence is synchronous, but that does not force the external HTTP client to be synchronous.

---

# Error model to plan for

Do not allow arbitrary HTTP-library exceptions to leak into profiler/domain code.

Potential normalized transport/domain failures:

```text
RiotAuthenticationError
RiotNotFoundError
RiotRateLimitedError
RiotServiceUnavailableError
RiotTransportError
RiotInvalidResponseError
```

Exact names are not final.

## HTTP handling

Riot documents common API responses including:

```text
400
401
403
404
415
429
5xx
```

### 429

On rate limiting, Riot instructs clients to respect the:

```text
Retry-After
```

header and halt requests for that duration.

Riot describes three API infrastructure rate-limit categories:

```text
application
method
service
```

There can also be limits in underlying services that return 429 without the usual API-edge rate-limit-type header.

Do not implement retries as an unconditional immediate loop.

### 5xx

Use bounded retry/backoff for temporary service failures.

Never turn a Riot outage into:

```text
player does not exist
```

Infrastructure errors and domain absence must remain distinct.

---

# API key constraints

## Development key

Riot documentation states that development keys:

```text
expire every 24 hours
```

This is fine for M1 exploration but must not be treated as a production credential model.

## Personal key

Riot currently documents personal-key limits of:

```text
20 requests / 1 second
100 requests / 2 minutes
```

with rate limiting enforced per region.

Production limits differ and are application-specific.

### SynapseCORD implication

The profiler architecture must assume API calls are a constrained resource.

This reinforces the existing design:

```text
Discord
→ profiling job
→ profiler worker
→ Riot provider
```

rather than calling large Riot histories inline during Discord command execution.

---

# Request-volume model

A full profile can become expensive quickly.

Example conceptual history of 50 matches:

```text
1 account lookup
1 match-ID request
50 match-detail requests
+ up to 50 timeline requests
+ ranked lookup
+ mastery lookup
```

This means timeline usage should be evidence-driven.

Before M3 we should estimate:

```text
requests/profile
payload bytes/profile
processing time/profile
useful evidence gained per endpoint
```

---

# M1 empirical reconnaissance plan

Use a small test script/CLI rather than immediately embedding calls into Discord.

## Test account set

Ideally include several account profiles:

```text
A. normal active ranked account
B. unranked / low-history account
C. account with Solo + Flex
D. account with varied game modes
E. optional high-volume / old account
```

Do not commit personally identifying raw payloads to the repository.

Use sanitized fixtures where persistent payload samples are useful.

---

## Phase A — Identity

### Test 1

```text
Riot ID + platform
→ ACCOUNT-V1
→ PUUID
```

Record:

```text
status
routing
response shape
errors
```

### Test 2

```text
PUUID
→ ACCOUNT-V1
→ current Riot ID
```

Verify round-trip identity.

### Test 3

```text
PUUID + platform
→ SUMMONER-V4
```

Check what League-specific identifiers and metadata are currently returned.

---

## Phase B — History

### Test 4

```text
PUUID
→ MATCH-V5 IDs
```

Try:

```text
default
count-limited
time-limited
queue-filtered
```

Record ordering and boundary behavior.

### Test 5

Fetch several different MatchDto samples:

```text
ranked Solo
ranked Flex
normal
short/remake if available
other mode
```

Compare participant schemas.

---

## Phase C — Timeline

### Test 6

Fetch timelines for the same sampled matches.

Build an inventory of:

```text
frame fields
event types
participant fields
position data
timestamps
```

Identify which M3 candidate features genuinely need timeline data.

---

## Phase D — Ranked / mastery

### Test 7

```text
PUUID
→ League entries
```

Validate unranked vs multi-queue behavior.

### Test 8

```text
PUUID
→ Champion Mastery
```

Compare:

```text
historical mastery
vs
champions actually played in recent history
```

---

# Payload research notes to capture

For each endpoint/sample record:

```text
Endpoint:
Routing:
Request params:
HTTP status:
Response size:
Top-level DTO:
Optional fields observed:
Zero/empty fields omitted:
Unexpected fields:
Patch / queue:
SynapseCORD value:
Needs timeline?:
Normalization idea:
Open questions:
```

---

# M3 questions that API reconnaissance must answer

The API layer is not the profiling model. Before defining `ObservedFeatureVector`, answer these with data:

```text
Can early aggression be measured reliably?
Can roaming be measured reliably?
Can resource dependence be measured without role/champion bias?
Can fight participation be separated from simply winning?
Can objective participation be reconstructed consistently?
Is vision activity comparable across roles?
How reliable are Riot role/position labels?
Which `challenges` values are stable enough to depend on?
Which metrics need timeline data?
How much history is enough for each feature?
How strongly must features be normalized by role/champion/rank?
```

Do not finalize behavioral scoring until these questions have empirical evidence.

---

# Proposed implementation sequence after reconnaissance

```text
M1.1
routing + RiotApiClient

M1.2
ACCOUNT-V1 identity lookup

M1.3
SUMMONER-V4 League context

M1.4
MATCH-V5 history IDs

M1.5
MATCH-V5 match detail

M1.6
MATCH-V5 timeline

M1.7
LEAGUE-V4 rank context

M1.8
CHAMPION-MASTERY-V4 context

M1.9
normalized League models

M1.10
fixtures + provider tests
```

Only after payload reconnaissance should M3's actual feature schema be fixed.

---

# Current conclusions

Confirmed direction:

```text
Riot ID is the onboarding/player-facing identifier.
PUUID is SynapseCORD's stable League external identity.
Platform must currently be known/configured for League shard APIs.
MATCH-V5 is the main observed-behavior source.
Timeline is potentially valuable but must justify its request cost.
LEAGUE-V4 provides context/constraints, not behavioral identity.
Champion Mastery provides historical affinity, not recent behavior.
Raw Riot DTOs must stop at the League adapter boundary.
```

The official documentation is sufficient to proceed with M1 architecture.

Real API payloads are still required before finalizing M3 feature extraction.

---

# Official sources

Reviewed 2026-09-24:

- Riot Developer Portal — League of Legends documentation  
  https://developer.riotgames.com/docs/lol

- Riot Developer Portal — API Reference  
  https://developer.riotgames.com/apis

- Riot Developer Portal — Web APIs / API keys / rate limiting  
  https://developer.riotgames.com/docs/portal

- Riot Developer Portal — Summoner Name to Riot ID FAQ  
  https://developer.riotgames.com/docs/summoner-name-to-riot-id-faq

- Riot Developer Portal — General policies  
  https://developer.riotgames.com/policies/general

- Riot Developer Portal — Game-specific policies  
  https://developer.riotgames.com/policies/game-specific

## Maintenance rule

Before implementing a Riot endpoint, re-check the live API Reference.

Riot APIs, DTOs, rate limits, routing and policies may change independently of SynapseCORD.
