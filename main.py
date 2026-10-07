from config.cities import CITIES
from src.ingestion.weather_api import get_weather,save_raw_data

def main():
    print("Weather Data Engineering Pipeline started")
    for city in CITIES:
        print(f"Fetching weather data for city:-{city}...")
        weather_data=get_weather(city)
        save_raw_data(weather_data,city)
        
    print("Weather data ingestion completed successfully.")

if __name__=="__main__":
    main()