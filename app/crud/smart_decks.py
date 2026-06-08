from sqlalchemy.orm import Session
from app.models.smart_decks import SmartDeck
from app.schemas.smart_decks import SmartDeckCreate
from typing import List, Optional

def get_smart_deck(db: Session, deck_id: str) -> Optional[SmartDeck]:
    return db.query(SmartDeck).filter(SmartDeck.id == deck_id).first()

def get_smart_decks_by_user(db: Session, user_id: str) -> List[SmartDeck]:
    return db.query(SmartDeck).filter(SmartDeck.user_id == user_id).all()

def create_smart_deck(db: Session, deck: SmartDeckCreate) -> SmartDeck:
    db_deck = SmartDeck(**deck.model_dump())
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck

def delete_smart_deck(db: Session, deck_id: str) -> bool:
    db_deck = get_smart_deck(db, deck_id)
    if db_deck:
        db.delete(db_deck)
        db.commit()
        return True
    return False
