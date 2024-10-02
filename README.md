# Weather API

## Overview
This project is a Flask-based RESTful API that provides weather information for specified cities. It fetches data from a third-party weather service, caches responses, and implements rate limiting to ensure efficient and controlled access to weather data.

## Features
- Fetch current weather data for any city
- Caching mechanism using Redis to improve response times and reduce API calls
- Rate limiting to prevent abuse of the service
- Error handling for various scenarios
- Environment variable configuration for sensitive data

## Setup
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up a Redis server
4. Create a `.env` file with the following variables:
   ```
   WEATHER_API_KEY=your_api_key_here
   WEATHER_API_URL=https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline
   ```

## Usage
1. Start the Flask application:
   ```
   python app.py
   ```
2. Access the API at `http://localhost:5000`
3. To get weather data for a city, make a GET request to:
   ```
   GET /weather/<city_name>
   ```

## API Endpoints
- `GET /`: Welcome message and usage instructions
- `GET /weather/<city>`: Retrieve weather data for the specified city

src: https://roadmap.sh/projects/weather-api-wrapper-service