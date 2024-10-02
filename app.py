from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from datetime import timedelta
import redis
import json
import logging
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Get API key and base URL from environment variables
API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = os.getenv('WEATHER_API_URL')

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize rate limiter with Redis storage
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379",
    default_limits=["200 per day", "50 per hour"]
)

# Function to get cached weather data for a city
def get_cached_weather(city):
    cached_data = r.get(city)
    return json.loads(cached_data) if cached_data else None

# Function to cache weather data for a city
def set_cached_weather(city, weather_data):
    # Cache data for 1 hour
    r.setex(city, timedelta(hours=1), json.dumps(weather_data))

# Function to fetch weather data from the API
def fetch_from_api(city):
    response = requests.get(f'{BASE_URL}/{city}?unitGroup=metric&key={API_KEY}')
    response.raise_for_status()
    return response.json()

# Function to process and format weather data
def process_weather_data(data):
    return {
        'city': data['address'],
        'temperature': {
            'celsius': data['currentConditions']['temp'],
            'fahrenheit': (data['currentConditions']['temp'] * 9/5) + 32
        },
        'description': data['currentConditions']['conditions'],
        'humidity': data['currentConditions']['humidity'],
        'wind_speed': data['currentConditions']['windspeed']
    }

# Route to get weather data for a city
@app.route('/weather/<string:city>', methods=['GET'])
@limiter.limit("5 per minute")  # Rate limit: 5 requests per minute
def get_weather(city):
    try:
        # Check if city name is provided
        if not city:
            raise ValueError('City name is required')
        
        # Try to get cached data
        cached_data = get_cached_weather(city)
        if cached_data:
            return jsonify(cached_data), 200
        
        # If not cached, fetch from API
        weather_data = fetch_from_api(city)
        # Process the fetched data
        processed_data = process_weather_data(weather_data)
        # Cache the processed data
        set_cached_weather(city, processed_data)

        return jsonify(processed_data), 200
    except ValueError as ve:
        # Handle invalid input
        logging.error(f'Value error: {str(ve)}')
        return jsonify({"error": str(ve)}), 400
    except requests.RequestException as re:
        # Handle API request errors
        logging.error(f'Request exception: {re}')
        return jsonify({"error": "Unable to reach weather service"}), 503
    except redis.RedisError as re:
        # Handle Redis errors
        logging.error(f'Redis error: {str(re)}')
        return jsonify({"error": "Cache service unavailable"}), 503
    except Exception as e:
        # Handle unexpected errors
        logging.error(f'Unexpected error: {str(e)}')
        return jsonify({"error": "An unexpected error occurred"}), 500

# Route for the root URL
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Weather API",
        "usage": "GET /weather/<city> to retrieve weather data for a specific city"
    }), 200

if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)