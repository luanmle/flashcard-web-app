from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# User Schemas
# ==========================================
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ==========================================
# Topic Schemas
# ==========================================
class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TopicResponse(TopicBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ==========================================
# Subtopic Schemas
# ==========================================
class SubtopicBase(BaseModel):
    name: str
    description: Optional[str] = None
    topic_id: str

class SubtopicCreate(SubtopicBase):
    pass

class SubtopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    topic_id: Optional[str] = None

class SubtopicResponse(SubtopicBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ==========================================
# Deck Schemas
# ==========================================
class DeckBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = False
    user_id: str

class DeckCreate(DeckBase):
    pass

class DeckUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class DeckResponse(DeckBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ==========================================
# Card Schemas
# ==========================================
class CardBase(BaseModel):
    deck_id: str
    subtopic_id: str
    front_content: str
    back_content: str
    explanation: Optional[str] = None
    tags: Optional[str] = None
    card_type: str = "basic"

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    front_content: Optional[str] = None
    back_content: Optional[str] = None
    explanation: Optional[str] = None
    tags: Optional[str] = None
    card_type: Optional[str] = None

class CardResponse(CardBase):
    id: str
    created_at: datetime

    # Extended properties for breadcrumbs when queried directly
    deck_title: Optional[str] = None
    subtopic_name: Optional[str] = None
    topic_name: Optional[str] = None

    model_config = {"from_attributes": True}

# ==========================================
# User Card Annotation Schemas
# ==========================================
class UserCardAnnotationBase(BaseModel):
    user_id: str
    card_id: str
    text: str

class UserCardAnnotationCreate(UserCardAnnotationBase):
    pass

class UserCardAnnotationUpdate(BaseModel):
    text: str

class UserCardAnnotationResponse(UserCardAnnotationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# ==========================================
# Card Suggestion Schemas
# ==========================================
class CardSuggestionBase(BaseModel):
    user_id: str
    card_id: str
    comment: str
    suggested_front: Optional[str] = None
    suggested_back: Optional[str] = None
    status: str = "pending"

class CardSuggestionCreate(CardSuggestionBase):
    pass

class CardSuggestionUpdate(BaseModel):
    status: str

class CardSuggestionResponse(CardSuggestionBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ==========================================
# User Card State Schemas (SRS)
# ==========================================
class UserCardStateBase(BaseModel):
    user_id: str
    card_id: str
    interval: int = 0
    easiness_factor: float = 2.5
    next_review_date: datetime

class UserCardStateCreate(UserCardStateBase):
    pass

class UserCardStateUpdate(BaseModel):
    interval: Optional[int] = None
    easiness_factor: Optional[float] = None
    next_review_date: Optional[datetime] = None

class UserCardStateResponse(UserCardStateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ==========================================
# Review Schemas
# ==========================================
class ReviewBase(BaseModel):
    user_id: str
    card_id: str
    rating: int = Field(..., ge=1, le=4)
    duration_ms: int

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=4)
    duration_ms: Optional[int] = None

class ReviewResponse(ReviewBase):
    id: str
    reviewed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
