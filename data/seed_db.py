import json
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud import user as crud_user
from app.crud import topic as crud_topic
from app.crud import subtopic as crud_subtopic
from app.crud import card as crud_card
from app.crud import smart_decks as crud_smart_decks
from app.schemas.flashcards import (
    UserCreate, TopicCreate, SubtopicCreate, CardCreate
)
from app.schemas.smart_decks import SmartDeckCreate

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

                for card_data in subtopic_data.get("cards", []):
                    # 4. Create or Get Card
                    # Idempotency check: look if a card with the exact front_content exists in this subtopic
                    db_cards = crud_card.get_cards_by_subtopic(db, subtopic_id=db_subtopic.id)
                    db_card = next((c for c in db_cards if c.front_content == card_data["front_content"]), None)
                    if not db_card:
                        print(f"    Creating card: {card_data['front_content'][:30]}...")
                        card_in = CardCreate(
                            subtopic_id=db_subtopic.id,
                            front_content=card_data["front_content"],
                            back_content=card_data["back_content"],
                            tags=card_data.get("tags"),
                            card_type=card_data.get("card_type", "basic")
                        )
                        crud_card.create_card(db, card_in)
                    else:
                        print(f"    Card '{card_data['front_content'][:30]}...' already exists.")

        # Create a default SmartDeck for the user
        smart_decks = crud_smart_decks.get_smart_decks_by_user(db, user_id=db_user.id)
        if not any(sd.name == "Todos os Cartões de Pandas" for sd in smart_decks):
            print("  Creating SmartDeck: Todos os Cartões de Pandas")
            db_topic = crud_topic.get_topic_by_name(db, name="Ciência de Dados")
            if db_topic:
                db_subtopics = crud_subtopic.get_subtopics_by_topic(db, topic_id=db_topic.id)
                pandas_subtopic = next((st for st in db_subtopics if st.name == "Pandas"), None)
                if pandas_subtopic:
                    sd_in = SmartDeckCreate(
                        user_id=db_user.id,
                        name="Todos os Cartões de Pandas",
                        filter_criteria={"subtopic_id": pandas_subtopic.id}
                    )
                    crud_smart_decks.create_smart_deck(db, sd_in)

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
