import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """
    Fetch current weather data for a given city.
    """

    params={
        "q":city,
        "appid":API_KEY,
        "units":"metric"
    }

    response=requests.get(BASE_URL,params=params,timeout=30)

    response.raise_for_status()

    return response.json()

def save_raw_data(data,city):
    """
    Save API responses as a raw JSON
    """

    timestamp=datetime.now().strftime("%d-%m-%Y_%H%M%S")

    filename=f"{city}_{timestamp}.json"

    filepath = os.path.join("data", "raw", filename)

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Raw weather data saved to: {filepath}")



