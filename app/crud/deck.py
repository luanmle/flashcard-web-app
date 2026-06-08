from sqlalchemy.orm import Session
from app.models.flashcards import Deck
from app.schemas.flashcards import DeckCreate, DeckUpdate
from typing import List, Optional

def get_deck(db: Session, deck_id: str) -> Optional[Deck]:
    return db.query(Deck).filter(Deck.id == deck_id).first()

def get_decks(db: Session, skip: int = 0, limit: int = 100) -> List[Deck]:
    return db.query(Deck).offset(skip).limit(limit).all()

def get_decks_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Deck]:
    return db.query(Deck).filter(Deck.user_id == user_id).offset(skip).limit(limit).all()

def create_deck(db: Session, deck: DeckCreate) -> Deck:
    db_deck = Deck(**deck.model_dump())
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck

def update_deck(db: Session, db_deck: Deck, deck_update: DeckUpdate) -> Deck:
    update_data = deck_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_deck, key, value)
    db.commit()
    db.refresh(db_deck)
    return db_deck

def delete_deck(db: Session, deck_id: str) -> bool:
    db_deck = get_deck(db, deck_id)
    if db_deck:
        db.delete(db_deck)
        db.commit()
        return True
    return False
