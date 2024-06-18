from ..database import SessionLocal
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models.sensor import SensorData


# Helper function to get the latest timestamp in the database
def get_latest_timestamp(db: Session):
    latest_entry = db.query(func.max(SensorData.timestamp)).scalar()
    if latest_entry is None:
        raise HTTPException(status_code=404, detail="No data available")
    return latest_entry


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
