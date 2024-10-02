import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = os.getenv('WEATHER_API_URL')

def test_weather_api(location):
    url = f"{BASE_URL}/{location}?unitGroup=metric&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Weather data for {location}:")
        print(f"Temperature: {data['currentConditions']['temp']}°C")
        print(f"Conditions: {data['currentConditions']['conditions']}")
        print(f"Humidity: {data['currentConditions']['humidity']}%")
    else:
        print(f"Error: Unable to fetch weather data. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Test with a specific location
test_weather_api("London,UK")