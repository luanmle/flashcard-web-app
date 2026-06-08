from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user_card_state as crud_state
from app.schemas.flashcards import UserCardStateResponse

router = APIRouter()

@router.get("/due/{user_id}", response_model=List[UserCardStateResponse])
def get_due_cards(
    user_id: str,
    deck_id: Optional[str] = Query(None, description="Filter due cards by a specific deck"),
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Returns all UserCardState records that have a next_review_date in the past
    or present, meaning they are due for review by the specified user.
    Optional deck_id filtering is supported.
    """
    due_cards = crud_state.get_due_cards_for_user(db=db, user_id=user_id, limit=limit, deck_id=deck_id)
    return due_cards
