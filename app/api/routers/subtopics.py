from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import subtopic as crud_subtopic
from app.schemas.flashcards import SubtopicCreate, SubtopicResponse, SubtopicUpdate

router = APIRouter()

@router.post("/", response_model=SubtopicResponse)
def create_subtopic(subtopic_in: SubtopicCreate, db: Session = Depends(get_db)):
    return crud_subtopic.create_subtopic(db=db, subtopic=subtopic_in)

@router.get("/", response_model=List[SubtopicResponse])
def read_subtopics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subtopics = crud_subtopic.get_subtopics(db, skip=skip, limit=limit)
    return subtopics

@router.get("/{subtopic_id}", response_model=SubtopicResponse)
def read_subtopic(subtopic_id: str, db: Session = Depends(get_db)):
    db_subtopic = crud_subtopic.get_subtopic(db, subtopic_id=subtopic_id)
    if db_subtopic is None:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return db_subtopic

@router.put("/{subtopic_id}", response_model=SubtopicResponse)
def update_subtopic(subtopic_id: str, subtopic_in: SubtopicUpdate, db: Session = Depends(get_db)):
    db_subtopic = crud_subtopic.get_subtopic(db, subtopic_id=subtopic_id)
    if db_subtopic is None:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return crud_subtopic.update_subtopic(db=db, db_subtopic=db_subtopic, subtopic_update=subtopic_in)

@router.delete("/{subtopic_id}", response_model=dict)
def delete_subtopic(subtopic_id: str, db: Session = Depends(get_db)):
    success = crud_subtopic.delete_subtopic(db, subtopic_id=subtopic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return {"detail": "Subtopic deleted successfully"}
