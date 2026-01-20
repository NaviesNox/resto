"""mengambil sesi database untuk dependensi"""
from app.core.database import SessionLocal
def get_db():
    """Mendapatkan sesi database untuk dependensi FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()