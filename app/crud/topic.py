from sqlalchemy.orm import Session
from app.models.flashcards import Topic
from app.schemas.flashcards import TopicCreate, TopicUpdate
from typing import List, Optional

def get_topic(db: Session, topic_id: str) -> Optional[Topic]:
    return db.query(Topic).filter(Topic.id == topic_id).first()

def get_topic_by_name(db: Session, name: str) -> Optional[Topic]:
    return db.query(Topic).filter(Topic.name == name).first()

def get_topics(db: Session, skip: int = 0, limit: int = 100) -> List[Topic]:
    return db.query(Topic).offset(skip).limit(limit).all()

def create_topic(db: Session, topic: TopicCreate) -> Topic:
    db_topic = Topic(**topic.model_dump())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def update_topic(db: Session, db_topic: Topic, topic_update: TopicUpdate) -> Topic:
    update_data = topic_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_topic, key, value)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(db: Session, topic_id: str) -> bool:
    db_topic = get_topic(db, topic_id)
    if db_topic:
        db.delete(db_topic)
        db.commit()
        return True
    return False
