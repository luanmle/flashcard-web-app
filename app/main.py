from fastapi import FastAPI
from app.api.routers import users, topics, subtopics, decks, cards, reviews, study

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flashcards API"}
