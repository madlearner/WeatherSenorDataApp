from datetime import datetime
from typing import List, Annotated, Optional
# from dependencies import get_token_header
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query, HTTPException, Depends
from ..schemas.sensor_data_request import SensorDataRequest
from ..models.sensor import SensorData
from ..services.service import get_sensor_data
from ..utills.helpers import get_db


# router = APIRouter(
#     prefix="/v1",
#     dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )

router = APIRouter(prefix="/v1")

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/sensor_data", tags=['Insert Sensor data'])
async def add_sensor_data(data: SensorDataRequest, db: db_dependency):
    # Validate data
    try:
        new_data = SensorData(
            sensor_id=data.sensor_id,
            temperature=data.temperature,
            humidity=data.humidity,
            pressure=data.pressure,
            wind_speed=data.wind_speed,
            latitude=data.latitude,
            longitude=data.longitude,
            timestamp=datetime.utcnow()
        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return {"message": "Sensor data added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/sensor_data", tags=['Get Sensor data'])
async def query_data(
    db: db_dependency,
    sensor_ids: List[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    statistics: List[str] = Query(None),
    metrics: List[str] = Query(None)
):
    try:
        params = {
            'db': db,
            'sensor_ids': sensor_ids,
            'start_date': start_date,
            'end_date': end_date,
            'statistics': statistics,
            'metrics': metrics
        }

        final_data = get_sensor_data(params)
        return final_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while querying data: {str(e)}")
