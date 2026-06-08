import csv
import json
from io import StringIO
from sqlalchemy.orm import Session
from app.crud import topic as crud_topic
from app.crud import subtopic as crud_subtopic
from app.crud import deck as crud_deck
from app.crud import card as crud_card
from app.schemas.flashcards import TopicCreate, SubtopicCreate, DeckCreate, CardCreate

def process_csv_import(db: Session, user_id: str, csv_data: str) -> dict:
    """
    Parses a CSV string and inserts cards.
    Expected CSV columns: topic, subtopic, deck, front, back, explanation, tags, card_type
    """
    f = StringIO(csv_data)
    reader = csv.DictReader(f)

    return _process_rows(db, user_id, reader)


def process_json_import(db: Session, user_id: str, json_data: str) -> dict:
    """
    Parses a JSON string array and inserts cards.
    Expected format:
    [
      {
        "topic": "...", "subtopic": "...", "deck": "...",
        "front": "...", "back": "...", "explanation": "...",
        "tags": "...", "card_type": "..."
      }
    ]
    """
    rows = json.loads(json_data)
    if not isinstance(rows, list):
        raise ValueError("JSON data must be a list of objects.")

    return _process_rows(db, user_id, rows)


def _process_rows(db: Session, user_id: str, rows) -> dict:
    stats = {
        "topics_created": 0,
        "subtopics_created": 0,
        "cards_created": 0,
        "cards_updated": 0,
        "errors": 0
    }

    # Simple caches to avoid repeated DB lookups during the loop
    topic_cache = {}
    subtopic_cache = {}

    for idx, row in enumerate(rows):
        try:
            topic_name = row.get("topic", "").strip()
            subtopic_name = row.get("subtopic", "").strip()
            front = row.get("front", "").strip()
            back = row.get("back", "").strip()

            if not topic_name or not subtopic_name or not front or not back:
                stats["errors"] += 1
                continue

            # 1. Resolve Topic
            if topic_name not in topic_cache:
                db_topic = crud_topic.get_topic_by_name(db, name=topic_name)
                if not db_topic:
                    db_topic = crud_topic.create_topic(db, TopicCreate(name=topic_name))
                    stats["topics_created"] += 1
                topic_cache[topic_name] = db_topic.id
            topic_id = topic_cache[topic_name]

            # 2. Resolve Subtopic
            subtopic_key = f"{topic_id}_{subtopic_name}"
            if subtopic_key not in subtopic_cache:
                db_subtopics = crud_subtopic.get_subtopics_by_topic(db, topic_id=topic_id, limit=1000000)
                db_subtopic = next((st for st in db_subtopics if st.name == subtopic_name), None)
                if not db_subtopic:
                    db_subtopic = crud_subtopic.create_subtopic(db, SubtopicCreate(name=subtopic_name, topic_id=topic_id))
                    stats["subtopics_created"] += 1
                subtopic_cache[subtopic_key] = db_subtopic.id
            subtopic_id = subtopic_cache[subtopic_key]

            # 3. Resolve Card (Upsert logic)
            # Idempotency check: see if exact card exists in this subtopic
            existing_cards = crud_card.get_cards_by_subtopic(db, subtopic_id=subtopic_id, limit=1000000)
            existing_card = next((c for c in existing_cards if c.front_content == front), None)

            from app.schemas.flashcards import CardUpdate

            if existing_card:
                # Update existing card
                update_data = CardUpdate(
                    back_content=back,
                    explanation=row.get("explanation"),
                    tags=row.get("tags"),
                    card_type=row.get("card_type", "basic") or "basic"
                )
                crud_card.update_card(db, db_card=existing_card, card_update=update_data)
                stats["cards_updated"] += 1
            else:
                # Create Card
                card_in = CardCreate(
                    subtopic_id=subtopic_id,
                    front_content=front,
                    back_content=back,
                    explanation=row.get("explanation"),
                    tags=row.get("tags"),
                    card_type=row.get("card_type", "basic") or "basic"
                )
                crud_card.create_card(db, card_in)
                stats["cards_created"] += 1

        except Exception as e:
            stats["errors"] += 1

    return stats
