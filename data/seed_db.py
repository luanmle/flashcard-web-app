import json
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud import user as crud_user
from app.crud import topic as crud_topic
from app.crud import subtopic as crud_subtopic
from app.crud import deck as crud_deck
from app.crud import card as crud_card
from app.schemas.flashcards import (
    UserCreate, TopicCreate, SubtopicCreate,
    DeckCreate, CardCreate
)

def load_seed_data(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def seed_database(db: Session, data: dict):
    print("Starting database seed...")
    for user_data in data.get("users", []):
        # 1. Create or Get User
        db_user = crud_user.get_user_by_email(db, email=user_data["email"])
        if not db_user:
            print(f"Creating user: {user_data['username']}")
            user_in = UserCreate(username=user_data["username"], email=user_data["email"])
            db_user = crud_user.create_user(db, user_in)
        else:
            print(f"User {user_data['username']} already exists. Skipping creation.")

        for topic_data in user_data.get("topics", []):
            # 2. Create or Get Topic
            db_topic = crud_topic.get_topic_by_name(db, name=topic_data["name"])
            if not db_topic:
                print(f"Creating topic: {topic_data['name']}")
                topic_in = TopicCreate(name=topic_data["name"], description=topic_data.get("description"))
                db_topic = crud_topic.create_topic(db, topic_in)
            else:
                print(f"Topic {topic_data['name']} already exists. Skipping creation.")

            for subtopic_data in topic_data.get("subtopics", []):
                # 3. Create or Get Subtopic
                # To be purely idempotent by name within a topic:
                db_subtopics = crud_subtopic.get_subtopics_by_topic(db, topic_id=db_topic.id)
                db_subtopic = next((st for st in db_subtopics if st.name == subtopic_data["name"]), None)
                if not db_subtopic:
                    print(f"  Creating subtopic: {subtopic_data['name']}")
                    subtopic_in = SubtopicCreate(
                        name=subtopic_data["name"],
                        description=subtopic_data.get("description"),
                        topic_id=db_topic.id
                    )
                    db_subtopic = crud_subtopic.create_subtopic(db, subtopic_in)
                else:
                    print(f"  Subtopic {subtopic_data['name']} already exists.")

                for deck_data in subtopic_data.get("decks", []):
                    # 4. Create or Get Deck
                    db_decks = crud_deck.get_decks_by_user(db, user_id=db_user.id)
                    db_deck = next((d for d in db_decks if d.title == deck_data["title"]), None)
                    if not db_deck:
                        print(f"    Creating deck: {deck_data['title']}")
                        deck_in = DeckCreate(
                            title=deck_data["title"],
                            description=deck_data.get("description"),
                            is_public=deck_data.get("is_public", False),
                            user_id=db_user.id
                        )
                        db_deck = crud_deck.create_deck(db, deck_in)
                    else:
                        print(f"    Deck {deck_data['title']} already exists.")

                    for card_data in deck_data.get("cards", []):
                        # 5. Create or Get Card
                        # Idempotency check: look if a card with the exact front_content exists in this deck
                        db_cards = crud_card.get_cards_by_deck(db, deck_id=db_deck.id)
                        db_card = next((c for c in db_cards if c.front_content == card_data["front_content"]), None)
                        if not db_card:
                            print(f"      Creating card: {card_data['front_content'][:30]}...")
                            card_in = CardCreate(
                                deck_id=db_deck.id,
                                subtopic_id=db_subtopic.id,
                                front_content=card_data["front_content"],
                                back_content=card_data["back_content"],
                                tags=card_data.get("tags"),
                                card_type=card_data.get("card_type", "basic")
                            )
                            crud_card.create_card(db, card_in)
                        else:
                            print(f"      Card '{card_data['front_content'][:30]}...' already exists.")

    print("Database seeding completed.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seed_file_path = os.path.join(current_dir, "seed.json")
        data = load_seed_data(seed_file_path)
        seed_database(db, data)
    finally:
        db.close()
