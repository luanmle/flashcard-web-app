from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user_card_state as crud_state
from app.schemas.flashcards import UserCardStateResponse

router = APIRouter()

from app.crud.smart_decks import get_smart_deck
from app.services.smart_decks import get_cards_for_smart_deck

@router.get("/due/{user_id}", response_model=List[UserCardStateResponse])
def get_due_cards(
    user_id: str,
    smart_deck_id: Optional[str] = Query(None, description="Filter due cards by a dynamic SmartDeck"),
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Returns all UserCardState records that have a next_review_date in the past
    or present, meaning they are due for review by the specified user.
    Optional smart_deck_id filtering is supported.
    """
    # 1. Fetch base due cards without deck restrictions
    # Since we decoupled decks, we fetch all user due cards first
    all_due_cards = crud_state.get_due_cards_for_user(db=db, user_id=user_id, limit=1000000)

    if not smart_deck_id:
        return all_due_cards[:limit]

    # 2. If a smart_deck filter is applied, resolve the SmartDeck criteria
    smart_deck = get_smart_deck(db, smart_deck_id)
    if not smart_deck:
        raise HTTPException(status_code=404, detail="Smart Deck not found")

    # 3. Get all valid card IDs matching the dynamic filter criteria
    valid_cards = get_cards_for_smart_deck(db, smart_deck.filter_criteria, limit=1000000)
    valid_card_ids = {c.id for c in valid_cards}

    # 4. Filter the due cards to only include those matching the SmartDeck criteria
    filtered_due_cards = [s for s in all_due_cards if s.card_id in valid_card_ids]

    return filtered_due_cards[:limit]
