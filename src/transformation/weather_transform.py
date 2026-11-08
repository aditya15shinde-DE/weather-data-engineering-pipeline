from datetime import datetime,timezone

def transform_weather_data(data):
    """
    Transform a validated weather API response 
    into a flat dictionary suitable for SQL Server
    """

    transformed_data={
        "city":data["name"].strip(),
        "temperature":float(data["main"]["temp"]),
        "humidity":int(data["main"]["humidity"]),
        "observation_time":datetime.fromtimestamp(
            data["dt"],tz=timezone.utc).replace(tzinfo=None)
    }

    return transformed_data


