from fastapi import FastAPI
from .routers import sensor_data
# from dependencies import get_query_token, get_token_header
# from internal import admin


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(title="Weather Sensor API",
    description="API for handling weather sensor data. Allows adding new sensor data and querying existing data.",
    version="1.0.0")

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     # dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )
app.include_router(sensor_data.router)
