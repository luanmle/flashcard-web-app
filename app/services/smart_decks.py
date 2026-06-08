from sqlalchemy.orm import Session
from app.models.flashcards import Card, Subtopic, Topic
from typing import List

def get_cards_for_smart_deck(db: Session, filter_criteria: dict, limit: int = 1000) -> List[Card]:
    """
    Dynamically filters the Card table based on the SmartDeck's JSON filter criteria.
    Supports filtering by topic_id, subtopic_id, and exact tags.
    """
    query = db.query(Card).join(Subtopic).join(Topic)

    if not filter_criteria:
        return query.limit(limit).all()

    topic_id = filter_criteria.get("topic_id")
    if topic_id:
        query = query.filter(Topic.id == topic_id)

    subtopic_id = filter_criteria.get("subtopic_id")
    if subtopic_id:
        query = query.filter(Subtopic.id == subtopic_id)

    tags = filter_criteria.get("tags")
    if tags:
        # A simple implementation for tags CSV string: ILIKE %tag%
        # In a real production app, consider an Array column instead of CSV strings
        # or use specialized full-text search.
        if isinstance(tags, str):
            query = query.filter(Card.tags.ilike(f"%{tags}%"))
        elif isinstance(tags, list):
            for tag in tags:
                query = query.filter(Card.tags.ilike(f"%{tag}%"))

    return query.limit(limit).all()
