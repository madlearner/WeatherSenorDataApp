from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class SensorDataRequest(BaseModel):
    sensor_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timestamp: datetime
