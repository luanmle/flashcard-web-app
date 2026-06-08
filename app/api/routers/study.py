from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user_card_state as crud_state
from app.schemas.flashcards import UserCardStateResponse

router = APIRouter()

@router.get("/due/{user_id}", response_model=List[UserCardStateResponse])
def get_due_cards(user_id: str, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns all UserCardState records that have a next_review_date in the past
    or present, meaning they are due for review by the specified user.
    """
    due_cards = crud_state.get_due_cards_for_user(db=db, user_id=user_id, limit=limit)
    return due_cards
