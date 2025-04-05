from sqlalchemy.orm import Session
from app.db.models import AudioClip
from app.schemas.clips import ClipCreate
from fastapi import HTTPException
from typing import List

def get_all_clips(db: Session) -> List[AudioClip]:
    return db.query(AudioClip).all()

def get_clip_by_id(db: Session, clip_id: int) -> AudioClip:
    clip = db.query(AudioClip).filter(AudioClip.id == clip_id).first()
    if not clip:
        raise HTTPException(status_code=404, detail=f"Clip with id {clip_id} not found")
    return clip

def create_clip(db: Session, clip_data: ClipCreate) -> AudioClip:
    db_clip = AudioClip(**clip_data.dict())
    db.add(db_clip)
    db.commit()
    db.refresh(db_clip)
    return db_clip

def increment_play_count(db: Session, clip_id: int) -> AudioClip:
    clip = get_clip_by_id(db, clip_id)
    clip.play_count += 1
    db.commit()
    db.refresh(clip)
    return clip

def get_clip_stats(db: Session, clip_id: int) -> AudioClip:
    return get_clip_by_id(db, clip_id)