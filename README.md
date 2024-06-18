# Weather Sensor Data

## Application Requirements
This service is designed to handle weather data from various sensors, which report metrics such as temperature, humidity, wind speed, etc. The main functionalities of the application include:

- **Receive Metric Values:** The application can receive new metric values via API calls as the weather changes around the sensor. The data gets added to the DB.
  
- **Query Sensor Data:** Users can query sensor data based on:
  - One or more sensors. If no query params provided it returns all the data from DB.
  - Metrics (e.g., temperature and humidity) to retrieve average, minimum, maximum, or sum values.
  - A specified date range (between one day and a month). If not specified, the data of the last 7 days are displayed.
  - Example Query: "Give me the average temperature and humidity for sensor 1 in the last week."

## Endpoints

### Add Sensor Data

**Endpoint:** `/v1/sensor_data`

**Method:** `POST`

**Description:** Adds new sensor data to the database.

## Request Body

- `sensor_id` (string, optional): The unique identifier of the sensor.
- `temperature` (float, optional): The temperature reading from the sensor.
- `humidity` (float, optional): The humidity reading from the sensor.
- `pressure` (float, optional): The pressure reading from the sensor.
- `wind_speed` (float, optional): The wind speed reading from the sensor.
- `latitude` (float, optional): The latitude where the sensor data was recorded.
- `longitude` (float, optional): The longitude where the sensor data was recorded.
- `timestamp` (datetime, optional): The timestamp when the data is added.

**Example Request:**
```json
{
  "sensor_id": "sensor_123",
  "temperature": 22.5,
  "humidity": 60.2,
  "pressure": 1013.25,
  "wind_speed": 5.5,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": "2024-06-18T21:54:34.722Z"
}
```

## Response

```json
{
  "message": "Sensor data added successfully"
}
```

## Query Sensor Data

**Endpoint:** `/v1/sensor_data`

**Method:** `GET`

**Description:** Retrieves sensor data based on query parameters.

**Query Parameters:**
- `sensor_ids` (List of strings, optional): List of sensor IDs to filter data.
- `start_date` (datetime, optional): Start date for the data range.
- `end_date` (datetime, optional): End date for the data range.
- `statistics` (List of strings, optional): List of statistics to apply to the data (e.g., average, max, min).
- `metrics` (List of strings, required): List of metrics to retrieve (e.g., temperature, humidity).

**Example Request:**

```bash
GET /v1/sensor_data?sensor_ids=sensor_123,sensor_456&start_date=2023-01-01T00:00:00Z&end_date=2023-12-31T23:59:59Z&statistics=average&metrics=temperature,humidity
```

## Example Response:

```json
{
  "sensor_data": [
    {
      "sensor_id": "sensor_123",
      "temperature": 22.5,
      "humidity": 60.2,
      "timestamp": "2023-06-18T14:35:00Z"
    },
    {
      "sensor_id": "sensor_456",
      "temperature": 23.1,
      "humidity": 59.8,
      "timestamp": "2023-06-18T14:35:00Z"
    }
  ],
  "statistics": {
    "average_temperature": 22.8,
    "average_humidity": 60.0
  }
}
```

## Error Handling

If an error occurs while processing your request, the API will return an appropriate HTTP status code and a JSON response containing the error details.

**Example Error Response:**

```json
{
  "detail": "An error occurred: Error message here"
}
```

## Technical Requirements
- **REST API:** The application is implemented as a REST API.
- **Programming Language:** Built with FastAPI using Python.
- **Source Code Repository:** The source code is publicly available on GitHub.
- **Database:** Application data is persisted in a PostgreSQL database.

## Setup Instructions
### To run the application, follow these steps:
1. Clone the Repository: `git clone https://github.com/madlearner/WeatherSenorDataApp.git`
   
### Set Up Virtual Environment:
- Create a virtual environment (optional but recommended): `python -m venv .env`
- Activate the virtual environment: `.env\Scripts\activate`
- Install the required dependencies: `pip install -r requirements.txt`

### Set Environment Variables:
- Using the `app/constants.py`, you can set up the environment variables of your DB.

## Usage

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```
The server will start running at http://localhost:8000 or http://127.0.0.1:8000.

## API Documentation

The API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) when the server is running.

## Testing

The project includes unit tests written using Python's `unittest` module and the `pytest` library. To run the tests, change directory to app, and execute the following command:

```bash
pytest tests
```
## Future Scope
We can add the token and admin,  in the current code it's the commented part.
It will be helpful for authentication and accessing the API.
`app\dependencies.py` contains token and secret which can be used (or replaced the values) for the future scope

