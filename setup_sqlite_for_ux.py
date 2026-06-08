from sqlalchemy import create_engine
from app.core.database import Base
import app.models.flashcards
import app.models.smart_decks

engine = create_engine('sqlite:///./test_fastapi.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine)
