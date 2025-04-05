import time
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import SessionLocal
from app.db.models import AudioClip, Base
from app.db.database import engine

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

def wait_for_db(retries=10, delay=2):
    for i in range(retries):
        try:
            session = SessionLocal()
            session.execute(text("SELECT 1"))
            session.close()
            print("✅ Database is ready!")
            return True
        except Exception as e:
            print(f"⏳ Waiting for DB... ({i + 1}/{retries}) | Error: {e}")
            time.sleep(delay)
    print("❌ Database not ready after retries.")
    return False

def seed_database():
    if not wait_for_db():
        print("❌ Exiting. Database not available.")
        return
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_clips = db.query(AudioClip).all()
        if existing_clips:
            print("⚠️  Database already contains clips. Skipping seed.")
            return

        for clip_data in SEED_CLIPS:
            db_clip = AudioClip(**clip_data)
            db.add(db_clip)
        db.commit()
        print(f"✅ Database seeded with {len(SEED_CLIPS)} clips.")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
