# tests/test_sensor_data.py

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import status
from app.routers.sensor_data import router
from app.schemas.sensor_data_request import SensorDataRequest

@pytest.fixture
def client():
    """
    Create a TestClient instance for testing.
    """
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    yield client

@patch('app.routers.sensor_data.Session')
def test_add_sensor_data_success(mock_session, client):
    """
    Test case for successfully adding sensor data.
    """
    mock_data = {
        "sensor_id": "sensor_2",
        "temperature": 45.6,
        "humidity": 34.5,
        "pressure": 1032,
        "wind_speed": 5.5,
        "latitude": 45.32,
        "longitude": 17.33,
        "timestamp": "2024-06-18T17:58:03.644Z"
    }

    mock_db = MagicMock()
    mock_session.return_value = mock_db
    response = client.post("/v1/sensor_data", json=mock_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Sensor data added successfully"}

@patch('app.routers.sensor_data.Session')
def test_add_sensor_data_failure(mock_session, client):
    """
    Test case for failure when adding sensor data.
    """
    mock_data = {
        "temperature": 45.6,
        "humidity": 34.5,
        "timestamp": "2024-06-18T17:58:03.644Z"
    }

    mock_db = MagicMock()
    mock_db.add.side_effect = Exception("Databse error")
    mock_session.return_value = mock_db

    response = client.post("/v1/sensor_data", json=mock_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'sensor_id'], 'msg': 'Field required', 'input': {'temperature': 45.6, 'humidity': 34.5, 'timestamp': '2024-06-18T17:58:03.644Z'}}]}


@patch('app.routers.sensor_data.get_sensor_data')
@patch('app.routers.sensor_data.Session')
def test_query_data_success(mock_session, mock_get_sensor_data, client):
    """
    Test case for successfully querying sensor data.
    """
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    
    mock_get_sensor_data.return_value = [
        {"sensor_id": "sensor_1", "temperature": 23.5, "humidity": 50.0, "pressure": 1015, "wind_speed": 3.4},
        {"sensor_id": "sensor_2", "temperature": 24.0, "humidity": 45.0, "pressure": 1013, "wind_speed": 4.1}
    ]

    params = {
        "sensor_ids": ["sensor_1", "sensor_2"],
        "statistics": ["average"],
        "metrics": ["temperature", "humidity"]
    }

    response = client.get("/v1/sensor_data", params=params)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"sensor_id": "sensor_1", "temperature": 23.5, "humidity": 50.0, "pressure": 1015, "wind_speed": 3.4},
        {"sensor_id": "sensor_2", "temperature": 24.0, "humidity": 45.0, "pressure": 1013, "wind_speed": 4.1}
    ]

@patch('app.routers.sensor_data.get_sensor_data')
@patch('app.routers.sensor_data.get_db')
def test_query_data_failure(mock_get_db, mock_get_sensor_data, client):
    """
    Test case for failure when querying sensor data.
    """
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    
    mock_get_sensor_data.side_effect = Exception("Query error")

    params = {
        "sensor_ids": ["sensor_1", "sensor_3"],
        "statistics": ["average"],
        "metrics": ["temperature", "humidity"]
    }

    response = client.get("/v1/sensor_data", params=params)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "An error occurred while querying data: Query error"}