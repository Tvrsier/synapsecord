from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class PlayerProfile:
    id: uuid.UUID
    game_account_id: uuid.UUID
    version: int
    status: str
    confidence: float | None
    valid_from: datetime
    superseded_at: datetime | None