# Flashcards API Platform

A robust backend API for a flashcards platform focused on data analysis and spaced repetition, built with FastAPI, SQLAlchemy, Alembic, and PostgreSQL.

## 🚀 Technologies

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Database:** PostgreSQL
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
* **Validation:** [Pydantic](https://docs.pydantic.dev/)

## 🏗️ Architecture

The project follows a clean and modular architectural design:

* `app/core/`: Contains core configurations (like the database connection).
* `app/models/`: SQLAlchemy ORM models representing the database schema.
* `app/schemas/`: Pydantic models for request/response validation.
* `app/crud/`: Reusable CRUD (Create, Read, Update, Delete) operations.
* `app/api/routers/`: FastAPI route definitions, handling HTTP logic and connecting with the CRUD layer.
* `app/main.py`: The entrypoint of the FastAPI application.
* `alembic/`: Database migration scripts and environment configurations.

### Key Entities
* **Users:** Unique profiles defined by an email and username.
* **Topics & Subtopics:** Hierarchical categorization for study subjects (e.g., 'Data Science' -> 'Pandas').
* **Decks:** Collections of flashcards authored by a User.
* **Cards:** Flashcards belonging to a Deck and a Subtopic, containing front/back content.
* **Reviews:** Telemetry data tracking user performance (`rating`, `duration_ms`) on specific cards for spaced repetition analytics.

All primary keys use auto-generated string UUIDs, and all tables track a `created_at` timestamp. Strict bidirectional ORM relationships are configured using `cascade="all, delete-orphan"` to guarantee referential integrity.

## 🛠️ Setup & Installation

### 1. Requirements
Ensure you have Python 3.12+ and PostgreSQL installed.

### 2. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
By default, the application connects to a local PostgreSQL database at `postgresql://postgres:postgres@localhost/flashcards`.
You can override this by exporting the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

### 4. Running Migrations
To initialize the database schema, apply the Alembic migrations:
```bash
alembic upgrade head
```

### 5. Running the Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## 📚 API Documentation

Once the server is running, FastAPI automatically generates interactive API documentation. You can explore the available endpoints and test them directly from your browser:

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

### Primary Endpoints
* **`/api/users/`**: Create, read, update, and delete Users.
* **`/api/topics/`**: Manage study Topics.
* **`/api/subtopics/`**: Manage Subtopics associated with Topics.
* **`/api/decks/`**: Manage flashcard Decks created by Users.
* **`/api/cards/`**: Manage individual Cards within Decks.
* **`/api/reviews/`**: Record and read Review logs for spaced repetition algorithms.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
