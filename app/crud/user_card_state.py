from sqlalchemy.orm import Session
from app.models.flashcards import UserCardState
from app.schemas.flashcards import UserCardStateCreate, UserCardStateUpdate
from typing import List, Optional
from datetime import datetime

def get_user_card_state(db: Session, state_id: str) -> Optional[UserCardState]:
    return db.query(UserCardState).filter(UserCardState.id == state_id).first()

def get_state_by_user_and_card(db: Session, user_id: str, card_id: str) -> Optional[UserCardState]:
    return db.query(UserCardState).filter(
        UserCardState.user_id == user_id,
        UserCardState.card_id == card_id
    ).first()

def get_due_cards_for_user(db: Session, user_id: str, limit: int = 100) -> List[UserCardState]:
    now = datetime.utcnow()
    return db.query(UserCardState).filter(
        UserCardState.user_id == user_id,
        UserCardState.next_review_date <= now
    ).order_by(UserCardState.next_review_date.asc()).limit(limit).all()

def create_user_card_state(db: Session, state: UserCardStateCreate) -> UserCardState:
    db_state = UserCardState(**state.model_dump())
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state

def update_user_card_state(db: Session, db_state: UserCardState, state_update: UserCardStateUpdate) -> UserCardState:
    update_data = state_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_state, key, value)
    db.commit()
    db.refresh(db_state)
    return db_state
