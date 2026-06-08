from datetime import datetime, timedelta

def calculate_next_review(rating: int, duration_ms: int, current_interval: int, current_ef: float):
    """
    Calculates the next review parameters based on an SM-2 inspired algorithm
    tuned with the user's hesitation (duration_ms).

    Rating scale:
    1 - Blackout (Complete failure)
    2 - Hard (Correct but with immense effort/hesitation)
    3 - Good (Correct with some hesitation)
    4 - Easy (Correct instantly)
    """
    # 1. Adjust Rating based on hesitation (duration_ms)
    # If the user answered "4" (Easy) but took more than 5 seconds (5000ms),
    # it probably wasn't that easy. We penalize the rating.
    adjusted_rating = rating
    if rating >= 3 and duration_ms > 8000:
        adjusted_rating = max(2, rating - 1)

    # 2. Calculate new Easiness Factor (EF)
    # SM-2 formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    # Where q is the 0-5 quality response. We map our 1-4 to roughly match.
    # We map: 1->1, 2->3, 3->4, 4->5
    q_map = {1: 1, 2: 3, 3: 4, 4: 5}
    q = q_map.get(adjusted_rating, 0)

    new_ef = current_ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))

    # Minimum EF is 1.3
    if new_ef < 1.3:
        new_ef = 1.3

    # 3. Calculate new Interval
    if adjusted_rating == 1:
        # Complete failure resets the interval
        new_interval = 1
    elif current_interval == 0:
        # First successful review
        new_interval = 1
    elif current_interval == 1:
        # Second successful review
        new_interval = 6
    else:
        # Subsequent reviews
        new_interval = round(current_interval * new_ef)

    # Calculate next review date
    next_review_date = datetime.utcnow() + timedelta(days=new_interval)

    return {
        "interval": new_interval,
        "easiness_factor": round(new_ef, 3),
        "next_review_date": next_review_date
    }
