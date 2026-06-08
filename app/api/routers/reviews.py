from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import review as crud_review
from app.crud import user_card_state as crud_state
from app.schemas.flashcards import ReviewCreate, ReviewResponse, ReviewUpdate, UserCardStateCreate, UserCardStateUpdate
from app.services.srs import calculate_next_review

router = APIRouter()

@router.post("/", response_model=ReviewResponse)
def create_review(review_in: ReviewCreate, db: Session = Depends(get_db)):
    # 1. Create the historical review log
    db_review = crud_review.create_review(db=db, review=review_in)

    # 2. Fetch or create current user card state
    state = crud_state.get_state_by_user_and_card(
        db=db,
        user_id=review_in.user_id,
        card_id=review_in.card_id
    )

    current_interval = state.interval if state else 0
    current_ef = state.easiness_factor if state else 2.5

    # 3. Calculate new SRS metrics
    new_srs_data = calculate_next_review(
        rating=review_in.rating,
        duration_ms=review_in.duration_ms,
        current_interval=current_interval,
        current_ef=current_ef
    )

    # 4. Update or Create the state
    if state:
        state_update = UserCardStateUpdate(
            interval=new_srs_data["interval"],
            easiness_factor=new_srs_data["easiness_factor"],
            next_review_date=new_srs_data["next_review_date"]
        )
        crud_state.update_user_card_state(db=db, db_state=state, state_update=state_update)
    else:
        state_create = UserCardStateCreate(
            user_id=review_in.user_id,
            card_id=review_in.card_id,
            interval=new_srs_data["interval"],
            easiness_factor=new_srs_data["easiness_factor"],
            next_review_date=new_srs_data["next_review_date"]
        )
        crud_state.create_user_card_state(db=db, state=state_create)

    return db_review

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
