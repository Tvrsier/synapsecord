from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class GameAccount:
    id: uuid.UUID
    user_id: uuid.UUID
    game_id: uuid.UUID
    external_id: str
    display_name: str
    region: str | None
    verified_at: datetime | None