# Weather Sensor Data

## Application Requirements
This service is designed to handle weather data from various sensors, which report metrics such as temperature, humidity, wind speed, etc. The main functionalities of the application include:

    Receive Metric Values: The application can receive new metric values via API calls as the weather changes around the sensor. The data gets added to the DB.

    Query Sensor Data: Users can query sensor data based on:

        - One or more sensors. If no query params provided it returns all the data from DB
        - Metrics (e.g., temperature and humidity) to retrieve average, minimum, maximum, or sum values.
        - A specified date range (between one day and a month). If not specified, the data of the last 7 days are displayed.
        - Example Query: "Give me the average temperature and humidity for sensor 1 in the last week."

# Technical Requirements
REST API: The application is implemented as a REST API 

Programming Language: Built with FastAPI using Python.

Source Code Repository: The source code is publicly available on GitHub 

Database: Application data is persisted in a PostgreSQL database.

# Setup Instructions

## To run the application, follow these steps:
> Clone the Repository: git clone 

> Set Up Virtual Environment: 
1. Create a virtual environment (optional but recommended): python -m venv .env
2. Activate the virtual environment: .env\Scripts\activate
3. Install the required dependencies: pip install -r requirements.txt

> Set Environment Variables:
Using the app/constants.py you can setup the environment variables of your DB

# Usage

> Start the FastAPI server:

command>> `uvicorn app.main:app --reload`

The server will start running at `http://localhost:8000` or `http://127.0.0.1:8000`

# API Documentation

The API documentation is available at `http://127.0.0.1:8000/docs` when the server is running.

# Testing

The project includes unit tests written using Python's `unittest` module and the `pytest` library. To run the tests, execute the following command: 
>> pytest 

## Future Scope
We can add the token and admin,  in the current code it's the commented part.
It will be helpful for authentication and accessing the API.
`app\dependencies.py` contains token and secret which can be used (or replaced the values) for the future scope
