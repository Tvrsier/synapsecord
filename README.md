<div align="center">

# SynapseCORD

**Player profiling and intelligent team matchmaking for competitive games.**

Build teams around how players actually play together — not only around rank and role availability.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-workspace-6E56CF)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00)
![Discord](https://img.shields.io/badge/Discord-Pycord%202.8.1-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## 🧠 Overview

SynapseCORD is a Discord-based platform for **player profiling, compatibility analysis and long-term team formation**.

The initial League of Legends implementation will combine:

- Riot API data
- in-chat player questionnaires
- behavioral and statistical profiling
- champion, role and playstyle synergy
- communication compatibility
- competitive preferences

The platform is designed to remain **game-agnostic at its core** so additional competitive games can be supported through adapters rather than by redesigning the system.

---

## 🧩 Core Idea

Most matchmaking systems are primarily designed to answer questions such as:

> *Which players can be placed together while satisfying constraints such as rank, role, availability and match quality?*

SynapseCORD aims to answer an additional question:

> *Which players are actually likely to work well together and synergize over time?*

Rather than replacing traditional matchmaking factors, SynapseCORD extends them with compatibility signals that are rarely considered when composing a team.

Compatibility can eventually consider dimensions such as:

- role compatibility
- resource expectations
- aggression and risk tolerance
- champion / character synergy
- communication style
- shotcalling preferences
- schedule compatibility
- competitive goals

The goal is not simply to assemble a valid or balanced team, but to build one whose members are more likely to complement each other strategically and interpersonally.

---

## 🏗️ Architecture

SynapseCORD is organized as a Python monorepo:

```text
synapsecord/
├── apps/
│   ├── bot/         # Discord interaction layer
│   └── profiler/    # profiling worker / CLI
├── packages/
│   └── core/        # shared domain, DB and infrastructure
├── migrations/
├── docs/
├── infra/
└── tests/
```

The Discord bot and profiling engine are intentionally separate applications:

```text
Discord Bot
    │
    ▼
profiling_jobs
    │
    ▼
Profiler Worker
    │
    ▼
PostgreSQL
```

This keeps the profiling and matchmaking domain independent from Discord.

---

## 🧬 Domain Resolution

Discord commands declare the domain data they require instead of performing persistence lookups directly.

Target command surface:

```python
@requires(User, GameAccount, PlayerProfile)
async def profile(ctx: SynapseApplicationContext) -> None:
    profile = ctx.player_profile
```

The framework is responsible for:

- registered domain resolution
- request-scoped caching
- dependency resolution
- circular dependency detection
- uniform missing-domain handling

Internally, resolved objects remain generic:

```python
ctx.domains.get(PlayerProfile)
ctx.domains.require(PlayerProfile)
```

while common domains are exposed through strongly typed context properties such as:

```python
ctx.user
ctx.game_account
ctx.player_profile
```

---

## ⚙️ Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.14 |
| Workspace | uv |
| Discord | Pycord 2.8.1 *(migration in progress)* |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2 |
| Migrations | Alembic |
| Configuration | Pydantic Settings |
| Logging | structlog |
| Testing | pytest |

---

## 🚧 Project Status

SynapseCORD is currently in **M0 — Foundation**.

### ✅ Implemented

- uv monorepo/workspace
- environment configuration
- structured logging
- PostgreSQL + SQLAlchemy foundation
- Alembic and initial schema
- repository layer
- profiler CLI foundation
- Discord bot foundation
- ServiceContainer
- DomainContext
- DomainResolver / DomainRegistry
- DomainResolutionService
- request-scoped domain caching
- circular domain-resolution protection
- domain framework test coverage

### 🔨 Current Focus

- migrate the Discord layer to Pycord 2.8.1
- implement `SynapseContext`
- implement `SynapseApplicationContext`
- introduce `SynapseAnyContext`
- build `@requires()` / `@inject()`
- request-scoped DB session lifecycle
- centralized Discord error handling

---

## 🗺️ Roadmap

```text
M0  Foundation
M1  Riot Integration
M2  Questionnaire
M3  League Feature Extractor
M4  Profiler v1
M5  Drift Detection
M6  Discord MVP
M7  Compatibility Engine
M8  Team Formation Engine
M9  Discord Team Management
M10 Team Learning
```

The long-term goal is to move from pairwise compatibility to **global team optimization** across an entire player pool.

---

## 🧭 Design Principles

- **Discord is an interaction layer**, not the domain core.
- Cogs should not scatter persistence queries across features.
- The profiler remains independent from Discord.
- Matching decisions are deterministic/statistical.
- LLMs may explain results, but do not decide team composition.
- New infrastructure is introduced only when justified.
- The platform should remain extensible to multiple competitive games.

---

## 🧪 Development

Install workspace dependencies:

```powershell
uv sync --all-packages
```

Run the domain framework tests:

```powershell
uv run pytest test/bot/domains
```

Check profiler/database health:

```powershell
uv run --package synapsecord-profiler synapsecord-profiler health
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
