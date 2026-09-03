from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from synapsecord_core.db.base import Base


class GameAccount(Base):
    __tablename__ = "game_accounts"
    
    __table_args__ = (
        UniqueConstraint(
            "game_id",
            "external_id",
            name="uq_game_accounts_game_external_id",
        ),
    )
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,        
        default=uuid.uuid4,
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    game_id: Mapped[str] = mapped_column(
        ForeignKey("games.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    region: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True
    )