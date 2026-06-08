from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class SmartDeckBase(BaseModel):
    user_id: str
    name: str
    filter_criteria: Dict[str, Any]

class SmartDeckCreate(SmartDeckBase):
    pass

class SmartDeckResponse(SmartDeckBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
