import pandas as pd
from src.database.connection import engine
from src.utils.logger import logger

def load_weather_data(records):
    if not records:
        logger.warning("No transformed weather records to load.")
        return 0

    df=pd.DataFrame(records)

    try:
        with engine.begin() as connection:
            df.to_sql(
                name="weather_data",
                con=connection,
                schema="dbo",
                if_exists="append",
                index=False,
                chunksize=500
                )

        logger.success(f"Successfully loaded {len(df)} weather records ")

        return len(df)

    except Exception:
        logger.exception("Failed to load weather records into SQL Server.")
        raise

    