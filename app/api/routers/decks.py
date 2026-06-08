from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import deck as crud_deck
from app.schemas.flashcards import DeckCreate, DeckResponse, DeckUpdate

router = APIRouter()

@router.post("/", response_model=DeckResponse)
def create_deck(deck_in: DeckCreate, db: Session = Depends(get_db)):
    return crud_deck.create_deck(db=db, deck=deck_in)

@router.get("/", response_model=List[DeckResponse])
def read_decks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    decks = crud_deck.get_decks(db, skip=skip, limit=limit)
    return decks

@router.get("/{deck_id}", response_model=DeckResponse)
def read_deck(deck_id: str, db: Session = Depends(get_db)):
    db_deck = crud_deck.get_deck(db, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck

@router.put("/{deck_id}", response_model=DeckResponse)
def update_deck(deck_id: str, deck_in: DeckUpdate, db: Session = Depends(get_db)):
    db_deck = crud_deck.get_deck(db, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return crud_deck.update_deck(db=db, db_deck=db_deck, deck_update=deck_in)

@router.delete("/{deck_id}", response_model=dict)
def delete_deck(deck_id: str, db: Session = Depends(get_db)):
    success = crud_deck.delete_deck(db, deck_id=deck_id)
    if not success:
        raise HTTPException(status_code=404, detail="Deck not found")
    return {"detail": "Deck deleted successfully"}
