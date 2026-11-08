
from config.cities import CITIES
from src.ingestion.weather_api import get_weather, save_raw_data
from src.utils.logger import logger
from src.validation.weather_validation import validate_weather
from src.validation.rejected_data import save_rejected_data
from src.transformation.weather_transform import transform_weather_data
from src.database.load_weather import load_weather_data


def main():
    logger.info("Weather Data Engineering Pipeline started")

    successful_cities = []
    failed_cities = []
    invalid_cities = []
    transformed_records = []

    for city in CITIES:
        logger.info(f"Fetching weather data for city: {city}")

        # Step 1: Fetch weather data
        weather_data = get_weather(city)

        if weather_data is None:
            failed_cities.append(city)
            logger.warning(f"Skipping raw data save for {city}")
            continue

        # Step 2: Save the original API response
        try:
            save_raw_data(weather_data, city)

        except Exception:
            failed_cities.append(city)
            logger.exception(
                f"Failed to save raw weather data for {city}"
            )
            continue

        # Step 3: Validate the weather data
        is_valid, errors = validate_weather(weather_data)

        if not is_valid:
            invalid_cities.append(city)

            logger.warning(
                f"Validation failed for {city}"
            )

            for error in errors:
                logger.warning(f"{city}: {error}")

            # Step 4: Save invalid data separately
            try:
                filepath = save_rejected_data(
                    weather_data,
                    city,
                    errors
                )

                logger.warning(
                    f"Rejected data saved to: {filepath}"
                )

            except Exception:
                failed_cities.append(city)

                logger.exception(
                    f"Failed to save rejected data for {city}"
                )

            # Do not process invalid data further
            continue

        # Step 5: Transform validated weather data
        try:
            transformed_data = transform_weather_data(weather_data)

            transformed_records.append(transformed_data)

            logger.info(
                f"Weather data transformed for {city}: "
                f"{transformed_data}"
            )

            successful_cities.append(city)

            logger.success(
                f"Weather data saved, validated, and transformed for {city}"
            )

        except Exception:
            failed_cities.append(city)

            logger.exception(
                f"Failed to transform weather data for {city}"
            )

    # Step 6: Load transformed records into SQL Server
    inserted_count = load_weather_data(transformed_records)

    logger.info(
        f"Database loading completed: {inserted_count} records inserted."
    )

    # Step 7: Print the pipeline summary
    print("\n========== PIPELINE SUMMARY ==========")
    print(f"Total cities         : {len(CITIES)}")
    print(f"Successful           : {len(successful_cities)}")
    print(f"Invalid              : {len(invalid_cities)}")
    print(f"Failed               : {len(failed_cities)}")
    print(f"Transformed records  : {len(transformed_records)}")

    if successful_cities:
        logger.info(
            f"Successful cities: {', '.join(successful_cities)}"
        )

    if invalid_cities:
        logger.warning(
            f"Invalid cities: {', '.join(invalid_cities)}"
        )

    if failed_cities:
        logger.warning(
            f"Failed cities: {', '.join(failed_cities)}"
        )

    # Step 8: Report execution status
    if failed_cities:
        logger.error(
            "Pipeline completed with failures. "
            f"Failed cities: {', '.join(failed_cities)}"
        )
        raise SystemExit(1)

    logger.info("Weather Data Engineering Pipeline completed")


if __name__ == "__main__":
    main()