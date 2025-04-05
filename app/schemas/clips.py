from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime

class ClipBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: str
    duration: float = Field(..., description="Duration in seconds")
    audio_url: str

class ClipCreate(ClipBase):
    pass

class Clip(ClipBase):
    id: int
    play_count: int = 0
    created_at: datetime
    
    class Config:
        orm_mode = True

class ClipStats(BaseModel):
    id: int
    title: str
    play_count: int
    genre: str
    duration: float
    
    class Config:
        orm_mode = True

class ClipsList(BaseModel):
    clips: List[Clip]
    
