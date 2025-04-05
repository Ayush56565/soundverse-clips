from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
from app.api.routes.clips import router as clips_router
from app.core.config import settings
from app.db.models import Base, AudioClip
from app.db.database import engine, SessionLocal
from sqlalchemy.orm import Session

def seed_data():
    db: Session = SessionLocal()
    try:
        existing = db.query(AudioClip).first()
        if existing:
            print("Seed data already exists. Skipping seeding.")
            return

        SEED_CLIPS = [
            {
                "title": "Ambient Forest",
                "description": "Peaceful forest ambience with birds and gentle wind",
                "genre": "ambient",
                "duration": 30.0,
                "audio_url": "https://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3"
            },
            {
                "title": "Electronic Beat",
                "description": "Upbeat electronic rhythm with synth pads",
                "genre": "electronic",
                "duration": 25.5,
                "audio_url": "https://codeskulptor-demos.commondatastorage.googleapis.com/GalaxyInvaders/theme_01.mp3"
            },
            {
                "title": "Acoustic Guitar",
                "description": "Solo acoustic guitar melody",
                "genre": "acoustic",
                "duration": 32.3,
                "audio_url": "https://codeskulptor-demos.commondatastorage.googleapis.com/pang/paza-moduless.mp3"
            },
            {
                "title": "Rain Sounds",
                "description": "Gentle rain falling on a rooftop",
                "genre": "ambient",
                "duration": 28.7,
                "audio_url": "https://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3"
            },
            {
                "title": "Jazz Piano",
                "description": "Smooth jazz piano improvisation",
                "genre": "jazz",
                "duration": 41.2,
                "audio_url": "https://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3"
            },
            {
                "title": "Tech House",
                "description": "Modern tech house with deep bass",
                "genre": "electronic",
                "duration": 35.6,
                "audio_url": "https://codeskulptor-demos.commondatastorage.googleapis.com/GalaxyInvaders/theme_01.mp3"
            }
        ]

        for clip in SEED_CLIPS:
            db.add(AudioClip(**clip))
        db.commit()
        print("Database seeded successfully.")
    except Exception as e:
        db.rollback()
        print("Error during seeding:", e)
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
seed_data()  

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    PrometheusMiddleware,
    app_name="clips_service",
    group_paths=True,
    prefix="clips_api",
)

app.add_route("/metrics", handle_metrics)
app.include_router(
    clips_router,
    prefix=f"{settings.API_V1_STR}/clips",
    tags=["clips"]
)

@app.get("/")
def root():
    return {"message": "Welcome to the Clips API Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
