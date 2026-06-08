from sqlalchemy.orm import Session
from app.models.flashcards import Card
from app.schemas.flashcards import CardCreate, CardUpdate
from typing import List, Optional

def get_card(db: Session, card_id: str) -> Optional[Card]:
    return db.query(Card).filter(Card.id == card_id).first()

def get_cards(db: Session, skip: int = 0, limit: int = 100) -> List[Card]:
    return db.query(Card).offset(skip).limit(limit).all()

def get_cards_by_subtopic(db: Session, subtopic_id: str, skip: int = 0, limit: int = 100) -> List[Card]:
    return db.query(Card).filter(Card.subtopic_id == subtopic_id).offset(skip).limit(limit).all()

def create_card(db: Session, card: CardCreate) -> Card:
    db_card = Card(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def update_card(db: Session, db_card: Card, card_update: CardUpdate) -> Card:
    update_data = card_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_card, key, value)
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, card_id: str) -> bool:
    db_card = get_card(db, card_id)
    if db_card:
        db.delete(db_card)
        db.commit()
        return True
    return False
