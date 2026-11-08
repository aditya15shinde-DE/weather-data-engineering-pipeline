
from sqlalchemy import text
from src.database.connection import engine
from src.utils.logger import logger


def create_weather_table():
    create_table_sql = """
    IF OBJECT_ID('dbo.weather_data', 'U') IS NULL
    BEGIN
        CREATE TABLE dbo.weather_data (
            id INT IDENTITY(1,1) PRIMARY KEY,
            city NVARCHAR(50) NOT NULL,
            temperature FLOAT NOT NULL,
            humidity INT NOT NULL,
            observation_time DATETIME2 NOT NULL

            
        );
    END;
    """

    with engine.begin() as connection:
        connection.execute(text(create_table_sql))

    print("Weather table created or already exists.")


if __name__ == "__main__":
    try:
        create_weather_table()
        logger.success("Weather table created or already exists.")

    except Exception:
        logger.exception("Failed to create weather table.")
        raise

    finally:
        engine.dispose()

