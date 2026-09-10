from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SynapseUser:
    id: uuid.UUID
    discord_user_id: int