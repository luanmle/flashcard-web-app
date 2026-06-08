from sqlalchemy.orm import Session
from app.models.flashcards import CardSuggestion
from app.schemas.flashcards import CardSuggestionCreate
from typing import List

def create_suggestion(db: Session, suggestion: CardSuggestionCreate) -> CardSuggestion:
    db_obj = CardSuggestion(**suggestion.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_suggestions_by_card(db: Session, card_id: str) -> List[CardSuggestion]:
    return db.query(CardSuggestion).filter(CardSuggestion.card_id == card_id).all()
