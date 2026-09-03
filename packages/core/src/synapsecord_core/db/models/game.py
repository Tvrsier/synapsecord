from __future__ import annotations

import uuid

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from synapsecord_core.db.base import Base


class Game(Base):
    __tablename__ = "games"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    
    slug: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )
    
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    
    enabled: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )