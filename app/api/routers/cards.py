from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import card as crud_card
from app.schemas.flashcards import CardCreate, CardResponse, CardUpdate

router = APIRouter()

@router.post("/", response_model=CardResponse)
def create_card(card_in: CardCreate, db: Session = Depends(get_db)):
    return crud_card.create_card(db=db, card=card_in)

@router.get("/", response_model=List[CardResponse])
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = crud_card.get_cards(db, skip=skip, limit=limit)
    return cards

@router.get("/{card_id}", response_model=CardResponse)
def read_card(card_id: str, db: Session = Depends(get_db)):
    db_card = crud_card.get_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    # We populate the extended properties for breadcrumbs dynamically
    response_data = CardResponse.model_validate(db_card)

    if db_card.subtopic:
        response_data.subtopic_name = db_card.subtopic.name
        if db_card.subtopic.topic:
            response_data.topic_name = db_card.subtopic.topic.name

    return response_data

@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: str, card_in: CardUpdate, db: Session = Depends(get_db)):
    db_card = crud_card.get_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return crud_card.update_card(db=db, db_card=db_card, card_update=card_in)

@router.delete("/{card_id}", response_model=dict)
def delete_card(card_id: str, db: Session = Depends(get_db)):
    success = crud_card.delete_card(db, card_id=card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"detail": "Card deleted successfully"}
