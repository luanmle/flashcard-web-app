from sqlalchemy.orm import Session
from app.models.flashcards import Review
from app.schemas.flashcards import ReviewCreate, ReviewUpdate
from typing import List, Optional

def get_review(db: Session, review_id: str) -> Optional[Review]:
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 100) -> List[Review]:
    return db.query(Review).offset(skip).limit(limit).all()

def get_reviews_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Review]:
    return db.query(Review).filter(Review.user_id == user_id).offset(skip).limit(limit).all()

def get_reviews_by_card(db: Session, card_id: str, skip: int = 0, limit: int = 100) -> List[Review]:
    return db.query(Review).filter(Review.card_id == card_id).offset(skip).limit(limit).all()

def create_review(db: Session, review: ReviewCreate) -> Review:
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, db_review: Review, review_update: ReviewUpdate) -> Review:
    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: str) -> bool:
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    return False
