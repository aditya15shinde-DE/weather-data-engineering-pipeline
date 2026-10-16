from config.cities import CITIES
from src.ingestion.weather_api import get_weather,save_raw_data
from src.utils.logger import logger

def main():
    logger.info("Weather Data Engineering Pipeline started")

    successful_cities=[]
    failed_cities=[]

    for city in CITIES:

        logger.info(f"Fetching weather data for city:-{city}...")

        weather_data=get_weather(city)
        if weather_data is None:
            failed_cities.append(city)
            logger.warning(f"Skipping raw data save for {city}")
            continue

        try:
            save_raw_data(weather_data,city)
            successful_cities.append(city)
            logger.success(f"Weather data saved for city:-{city}")

        except Exception:
            failed_cities.append(city)
            logger.exception("Failed to save weather data for {city}")

    print("\n========== PIPELINE SUMMARY ==========")
    print(f"Total cities     : {len(CITIES)}")
    print(f"Successful       : {len(successful_cities)}")
    print(f"Failed           : {len(failed_cities)}")

    if successful_cities:
        logger.info(f"Successful cities: {', '.join(successful_cities)}")

    if failed_cities:
        logger.warning(f"Failed cities    : {', '.join(failed_cities)}")

    logger.info("=======================================")    
    logger.info("Weather data ingestion completed successfully.")

if __name__=="__main__":
    main()