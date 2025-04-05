from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import requests
from fastapi.responses import StreamingResponse
from io import BytesIO
import time
from prometheus_client import Counter, Histogram

from app.db.database import get_db
from app.services.clips import (
    get_all_clips,
    get_clip_by_id,
    create_clip,
    increment_play_count,
    get_clip_stats
)
from app.schemas.clips import Clip, ClipCreate, ClipStats, ClipsList

router = APIRouter()

stream_counter = Counter(
    "clips_total_streams",
    "Total number of audio clip streams"
)

top_streamed_counter = Counter(
    "clips_top_streamed",
    "Top streamed clips by title and clip_id",
    ["clip_id", "title"]
)

stream_duration_histogram = Histogram(
    "clip_stream_duration_seconds",
    "Time taken to stream a clip",
    ["clip_id", "title"]
)

@router.get("/", response_model=List[Clip])
def list_clips(db: Session = Depends(get_db)):
    clips = get_all_clips(db)
    return clips

@router.get("/{clip_id}", response_model=Clip)
def get_clip(clip_id: int, db: Session = Depends(get_db)):
    return get_clip_by_id(db, clip_id)

@router.get("/{clip_id}/stream")
async def stream_clip(clip_id: int, db: Session = Depends(get_db)):
    clip = increment_play_count(db, clip_id)
    start_time = time.time()
    try:
        response = requests.get(clip.audio_url, stream=True)
        if response.status_code == 200:
            content = BytesIO(response.content)
            stream_counter.inc()
            top_streamed_counter.labels(clip_id=str(clip.id), title=clip.title).inc()
            stream_duration_histogram.labels(clip_id=str(clip.id), title=clip.title).observe(time.time() - start_time)
            return StreamingResponse(
                content=content, 
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename={clip.title}.mp3"}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve audio file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming file: {str(e)}")

@router.get("/{clip_id}/stats", response_model=ClipStats)
def get_clip_statistics(clip_id: int, db: Session = Depends(get_db)):
    return get_clip_stats(db, clip_id)

@router.post("/", response_model=Clip, status_code=201)
def add_clip(clip_data: ClipCreate, db: Session = Depends(get_db)):
    return create_clip(db, clip_data)
