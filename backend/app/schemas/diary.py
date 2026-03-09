from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class DiaryEntryCreate(BaseModel):
    content: str


class DiaryStructured(BaseModel):
    mood: str
    mood_score: int  # 1~10
    tags: list[str]
    summary: str
    key_events: list[str]


class DiaryEntryResponse(BaseModel):
    diary_id: int
    user_id: UUID
    content: str
    structured_data: Optional[dict] = None
    reflection: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
