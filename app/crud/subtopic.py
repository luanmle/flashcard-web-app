from sqlalchemy.orm import Session
from app.models.flashcards import Subtopic
from app.schemas.flashcards import SubtopicCreate, SubtopicUpdate
from typing import List, Optional

def get_subtopic(db: Session, subtopic_id: str) -> Optional[Subtopic]:
    return db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()

def get_subtopics(db: Session, skip: int = 0, limit: int = 100) -> List[Subtopic]:
    return db.query(Subtopic).offset(skip).limit(limit).all()

def get_subtopics_by_topic(db: Session, topic_id: str, skip: int = 0, limit: int = 100) -> List[Subtopic]:
    return db.query(Subtopic).filter(Subtopic.topic_id == topic_id).offset(skip).limit(limit).all()

def create_subtopic(db: Session, subtopic: SubtopicCreate) -> Subtopic:
    db_subtopic = Subtopic(**subtopic.model_dump())
    db.add(db_subtopic)
    db.commit()
    db.refresh(db_subtopic)
    return db_subtopic

def update_subtopic(db: Session, db_subtopic: Subtopic, subtopic_update: SubtopicUpdate) -> Subtopic:
    update_data = subtopic_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subtopic, key, value)
    db.commit()
    db.refresh(db_subtopic)
    return db_subtopic

def delete_subtopic(db: Session, subtopic_id: str) -> bool:
    db_subtopic = get_subtopic(db, subtopic_id)
    if db_subtopic:
        db.delete(db_subtopic)
        db.commit()
        return True
    return False
