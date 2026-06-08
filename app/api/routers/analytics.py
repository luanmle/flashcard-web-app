from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.analytics import get_user_analytics

router = APIRouter()

@router.get("/{user_id}")
def read_user_analytics(user_id: str, db: Session = Depends(get_db)):
    """
    Returns analytics metrics for the dashboard (Pandas processed).
    """
    data = get_user_analytics(db, user_id)
    return data
