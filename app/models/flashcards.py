import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    decks = relationship("Deck", back_populates="author", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    card_states = relationship("UserCardState", back_populates="user", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")

class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    topic_id = Column(String, ForeignKey("topics.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="subtopics")
    cards = relationship("Card", back_populates="subtopic", cascade="all, delete-orphan")

class Deck(Base):
    __tablename__ = "decks"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="decks")
    cards = relationship("Card", back_populates="deck", cascade="all, delete-orphan")

class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, default=generate_uuid)
    deck_id = Column(String, ForeignKey("decks.id"), nullable=False)
    subtopic_id = Column(String, ForeignKey("subtopics.id"), nullable=False)
    front_content = Column(Text, nullable=False)
    back_content = Column(Text, nullable=False)
    tags = Column(String, nullable=True) # Comma-separated
    card_type = Column(String, default="basic")
    created_at = Column(DateTime, default=datetime.utcnow)

    deck = relationship("Deck", back_populates="cards")
    subtopic = relationship("Subtopic", back_populates="cards")
    reviews = relationship("Review", back_populates="card", cascade="all, delete-orphan")
    user_states = relationship("UserCardState", back_populates="card", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    card_id = Column(String, ForeignKey("cards.id"), nullable=False)
    rating = Column(Integer, nullable=False) # 1 to 4
    duration_ms = Column(Integer, nullable=False)
    reviewed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    card = relationship("Card", back_populates="reviews")

class UserCardState(Base):
    __tablename__ = "user_card_states"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    card_id = Column(String, ForeignKey("cards.id"), nullable=False)

    interval = Column(Integer, default=0) # Interval in days
    easiness_factor = Column(Float, default=2.5) # SuperMemo-2 EF
    next_review_date = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="card_states")
    card = relationship("Card", back_populates="user_states")
