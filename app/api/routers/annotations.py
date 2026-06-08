from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import annotation as crud_annotation
from app.schemas.flashcards import UserCardAnnotationCreate, UserCardAnnotationUpdate, UserCardAnnotationResponse

router = APIRouter()

@router.get("/{user_id}/{card_id}", response_model=UserCardAnnotationResponse)
def get_annotation(user_id: str, card_id: str, db: Session = Depends(get_db)):
    db_obj = crud_annotation.get_annotation(db, user_id, card_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return db_obj

@router.post("/", response_model=UserCardAnnotationResponse)
def save_annotation(annotation_in: UserCardAnnotationCreate, db: Session = Depends(get_db)):
    db_obj = crud_annotation.get_annotation(db, annotation_in.user_id, annotation_in.card_id)
    if db_obj:
        # Update existing
        update_data = UserCardAnnotationUpdate(text=annotation_in.text)
        return crud_annotation.update_annotation(db, db_obj, update_data)
    else:
        # Create new
        return crud_annotation.create_annotation(db, annotation_in)
