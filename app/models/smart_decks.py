from sqlalchemy import Column, String, DateTime, ForeignKey, Index, JSON
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.core.database import Base
from app.models.flashcards import generate_uuid

# Use standard JSON as a fallback for SQLite testing, JSONB for Postgres
TypeJSON = JSON().with_variant(JSONB, "postgresql")

class SmartDeck(Base):
    __tablename__ = "smart_decks"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    # Stores dynamic filter rules like {"topics": ["id1", "id2"], "tags": ["math", "hard"]}
    filter_criteria = Column(TypeJSON, nullable=False, default={})

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # GIN index for optimal querying on JSONB properties (ignored by SQLite)
    __table_args__ = (
        Index('ix_smart_decks_filter_criteria_gin', filter_criteria, postgresql_using='gin'),
    )
