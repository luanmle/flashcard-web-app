import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any

def get_user_analytics(db: Session, user_id: str) -> Dict[str, Any]:
    """
    Computes analytics for a specific user using Pandas.
    - Average response time (duration_ms) grouped by Topic.
    - Hardest cards (Cards with the lowest average rating).
    - Review progress (Total reviews completed).
    """

    # 1. Fetch raw joined data for the user
    # We join Review -> Card -> Subtopic -> Topic
    query = text("""
        SELECT
            r.rating,
            r.duration_ms,
            c.front_content,
            t.name as topic_name
        FROM reviews r
        JOIN cards c ON r.card_id = c.id
        JOIN subtopics st ON c.subtopic_id = st.id
        JOIN topics t ON st.topic_id = t.id
        WHERE r.user_id = :user_id
    """)

    result = db.execute(query, {"user_id": user_id}).fetchall()

    # If no data, return empty structures
    if not result:
        return {
            "total_reviews": 0,
            "avg_duration_by_topic": {},
            "hardest_cards": []
        }

    # Load into Pandas DataFrame
    # Note: result is a list of tuples, so we map it to columns
    df = pd.DataFrame(result, columns=["rating", "duration_ms", "front_content", "topic_name"])

    # --- Metric 1: Total Reviews ---
    total_reviews = int(len(df))

    # --- Metric 2: Average Duration by Topic (in seconds for better readability) ---
    df['duration_sec'] = df['duration_ms'] / 1000.0
    duration_by_topic = df.groupby('topic_name')['duration_sec'].mean().round(2).to_dict()

    # --- Metric 3: Hardest Cards ---
    # Group by card content, find the mean rating, sort ascending (lowest rating = hardest)
    hardest_cards_df = df.groupby('front_content')['rating'].mean().round(2).reset_index()
    hardest_cards_df = hardest_cards_df.sort_values(by='rating').head(5)

    # Convert to list of dicts for the JSON response
    hardest_cards = hardest_cards_df.rename(columns={
        "front_content": "card_front",
        "rating": "avg_rating"
    }).to_dict(orient="records")

    return {
        "total_reviews": total_reviews,
        "avg_duration_by_topic": duration_by_topic,
        "hardest_cards": hardest_cards
    }
