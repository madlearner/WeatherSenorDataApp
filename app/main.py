from fastapi import FastAPI
from .routers import sensor_data
# from dependencies import get_query_token, get_token_header
# from internal import admin


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(title="Weather-Sensor-data")

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     # dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )
app.include_router(sensor_data.router)
