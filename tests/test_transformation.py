from src.transformation.weather_transform import transform_weather_data

sample_weather = {
    "name": " Pune ",
    "dt": 1792150000,
    "main": {
        "temp": 28.5,
        "humidity": 65
    }
}


flattened_json=transform_weather_data(sample_weather)
print("Transformed weather data:")
print(flattened_json)

assert flattened_json["city"] == "Pune"
assert flattened_json["temperature"] == 28.5
assert flattened_json["humidity"] == 65
assert flattened_json["observation_time"].year == 2026


print("\nPASS: Weather transformation test completed.")