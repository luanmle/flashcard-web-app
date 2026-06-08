from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import review as crud_review
from app.schemas.flashcards import ReviewCreate, ReviewResponse, ReviewUpdate

router = APIRouter()

@router.post("/", response_model=ReviewResponse)
def create_review(review_in: ReviewCreate, db: Session = Depends(get_db)):
    return crud_review.create_review(db=db, review=review_in)

@router.get("/", response_model=List[ReviewResponse])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud_review.get_reviews(db, skip=skip, limit=limit)
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
def read_review(review_id: str, db: Session = Depends(get_db)):
    db_review = crud_review.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: str, review_in: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud_review.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return crud_review.update_review(db=db, db_review=db_review, review_update=review_in)

@router.delete("/{review_id}", response_model=dict)
def delete_review(review_id: str, db: Session = Depends(get_db)):
    success = crud_review.delete_review(db, review_id=review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"detail": "Review deleted successfully"}
