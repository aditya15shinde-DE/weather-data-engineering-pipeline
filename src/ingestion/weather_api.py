import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    
    
    if not API_KEY:
        logger.error("OPENWEATHER_API_KEY is missing from the .env file")
        return None

    try:
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
        logger.info(f"Weather data fetched successfully for {city}")

        return response.json()
    
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error while fetching weather data for {city}")
        return None

    except requests.exceptions.HTTPError as e:
        logger.error(f"API error while fetching weather data for {city}:- {e}")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {city}:{e}")
        return None
    
    except Exception as e:
        logger.exception(f"Unexpected error for {city}:{e}")
        return None

def save_raw_data(data,city):
    """
    Save API responses as a raw JSON
    """

    timestamp=datetime.now().strftime("%d-%m-%Y_%H%M%S")

    filename=f"{city}_{timestamp}.json"

    filepath = os.path.join("data", "raw", filename)

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

        logger.success(f"Raw weather data saved to: {filepath}")

    except OSError:
        logger.exception(f"Failed to save raw weather data for {city}")
        raise

    



