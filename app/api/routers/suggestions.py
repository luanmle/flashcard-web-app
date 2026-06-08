from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import suggestion as crud_suggestion
from app.schemas.flashcards import CardSuggestionCreate, CardSuggestionResponse

router = APIRouter()

@router.post("/", response_model=CardSuggestionResponse)
def create_suggestion(suggestion_in: CardSuggestionCreate, db: Session = Depends(get_db)):
    return crud_suggestion.create_suggestion(db, suggestion_in)
