from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import smart_decks as crud_smart_decks
from app.schemas.smart_decks import SmartDeckCreate, SmartDeckResponse

router = APIRouter()

@router.post("/", response_model=SmartDeckResponse)
def create_smart_deck(deck_in: SmartDeckCreate, db: Session = Depends(get_db)):
    return crud_smart_decks.create_smart_deck(db=db, deck=deck_in)

@router.get("/user/{user_id}", response_model=List[SmartDeckResponse])
def read_smart_decks(user_id: str, db: Session = Depends(get_db)):
    return crud_smart_decks.get_smart_decks_by_user(db, user_id=user_id)

@router.get("/{deck_id}", response_model=SmartDeckResponse)
def read_smart_deck(deck_id: str, db: Session = Depends(get_db)):
    db_deck = crud_smart_decks.get_smart_deck(db, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Smart Deck not found")
    return db_deck

@router.delete("/{deck_id}", response_model=dict)
def delete_smart_deck(deck_id: str, db: Session = Depends(get_db)):
    success = crud_smart_decks.delete_smart_deck(db, deck_id=deck_id)
    if not success:
        raise HTTPException(status_code=404, detail="Smart Deck not found")
    return {"detail": "Smart Deck deleted successfully"}
