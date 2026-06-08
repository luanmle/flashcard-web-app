from sqlalchemy.orm import Session
from app.models.flashcards import UserCardState, Card, Deck
from app.schemas.flashcards import UserCardStateCreate, UserCardStateUpdate, UserCardStateResponse
from typing import List, Optional
from datetime import datetime

def get_user_card_state(db: Session, state_id: str) -> Optional[UserCardState]:
    return db.query(UserCardState).filter(UserCardState.id == state_id).first()

def get_state_by_user_and_card(db: Session, user_id: str, card_id: str) -> Optional[UserCardState]:
    return db.query(UserCardState).filter(
        UserCardState.user_id == user_id,
        UserCardState.card_id == card_id
    ).first()

def get_due_cards_for_user(db: Session, user_id: str, limit: int = 100, deck_id: Optional[str] = None) -> List[UserCardStateResponse]:
    now = datetime.utcnow()

    # Base query for states
    state_query = db.query(UserCardState).join(Card).filter(
        UserCardState.user_id == user_id,
        UserCardState.next_review_date <= now
    )

    if deck_id:
        state_query = state_query.filter(Card.deck_id == deck_id)

    due_states = state_query.order_by(UserCardState.next_review_date.asc()).limit(limit).all()

    # Return types must match the Pydantic schema Response
    results = [UserCardStateResponse.model_validate(s) for s in due_states]

    # 2. Get "New" cards: Cards belonging to user's decks that lack a UserCardState
    if len(results) < limit:
        # Find card IDs the user already has a state for
        existing_state_card_ids = [s.card_id for s in db.query(UserCardState.card_id).filter(UserCardState.user_id == user_id).all()]

        # Find new cards in decks owned by the user
        remaining_limit = limit - len(results)

        new_cards_query = db.query(Card).join(Deck).filter(
            Deck.user_id == user_id
        )

        if deck_id:
            new_cards_query = new_cards_query.filter(Card.deck_id == deck_id)

        if existing_state_card_ids:
            new_cards_query = new_cards_query.filter(~Card.id.in_(existing_state_card_ids))

        new_cards = new_cards_query.limit(remaining_limit).all()

        # Wrap new cards in a pseudo UserCardStateResponse
        for nc in new_cards:
            pseudo_state = UserCardStateResponse(
                id="new_card_pseudo_id",
                user_id=user_id,
                card_id=nc.id,
                interval=0,
                easiness_factor=2.5,
                next_review_date=now,
                created_at=now,
                updated_at=now
            )
            results.append(pseudo_state)

    return results

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
