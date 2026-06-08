from sqlalchemy.orm import Session
from app.models.flashcards import UserCardAnnotation
from app.schemas.flashcards import UserCardAnnotationCreate, UserCardAnnotationUpdate
from typing import Optional

def get_annotation(db: Session, user_id: str, card_id: str) -> Optional[UserCardAnnotation]:
    return db.query(UserCardAnnotation).filter(
        UserCardAnnotation.user_id == user_id,
        UserCardAnnotation.card_id == card_id
    ).first()

def create_annotation(db: Session, annotation: UserCardAnnotationCreate) -> UserCardAnnotation:
    db_obj = UserCardAnnotation(**annotation.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_annotation(db: Session, db_obj: UserCardAnnotation, update_data: UserCardAnnotationUpdate) -> UserCardAnnotation:
    db_obj.text = update_data.text
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_annotation(db: Session, user_id: str, card_id: str) -> bool:
    db_obj = get_annotation(db, user_id, card_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False
