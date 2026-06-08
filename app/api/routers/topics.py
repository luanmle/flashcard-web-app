from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import topic as crud_topic
from app.schemas.flashcards import TopicCreate, TopicResponse, TopicUpdate

router = APIRouter()

@router.post("/", response_model=TopicResponse)
def create_topic(topic_in: TopicCreate, db: Session = Depends(get_db)):
    db_topic = crud_topic.get_topic_by_name(db, name=topic_in.name)
    if db_topic:
        raise HTTPException(status_code=400, detail="Topic name already registered")
    return crud_topic.create_topic(db=db, topic=topic_in)

@router.get("/", response_model=List[TopicResponse])
def read_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    topics = crud_topic.get_topics(db, skip=skip, limit=limit)
    return topics

@router.get("/{topic_id}", response_model=TopicResponse)
def read_topic(topic_id: str, db: Session = Depends(get_db)):
    db_topic = crud_topic.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic

@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: str, topic_in: TopicUpdate, db: Session = Depends(get_db)):
    db_topic = crud_topic.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return crud_topic.update_topic(db=db, db_topic=db_topic, topic_update=topic_in)

@router.delete("/{topic_id}", response_model=dict)
def delete_topic(topic_id: str, db: Session = Depends(get_db)):
    success = crud_topic.delete_topic(db, topic_id=topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"detail": "Topic deleted successfully"}
