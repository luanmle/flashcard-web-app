from fastapi import FastAPI
from app.api.routers import users, topics, subtopics, decks, cards, reviews, study, analytics, frontend

app = FastAPI(
    title="Flashcards API",
    description="API for the data analysis and spaced repetition flashcards platform.",
    version="1.0.0"
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(topics.router, prefix="/api/topics", tags=["topics"])
app.include_router(subtopics.router, prefix="/api/subtopics", tags=["subtopics"])
app.include_router(decks.router, prefix="/api/decks", tags=["decks"])
app.include_router(cards.router, prefix="/api/cards", tags=["cards"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(study.router, prefix="/api/study", tags=["study"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

# Include the frontend router without an API prefix
app.include_router(frontend.router, tags=["frontend"])
