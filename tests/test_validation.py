
from src.validation.weather_validation import validate_weather


valid_weather = {
    "name": "Pune",
    "main": {
        "temp": -23,
        "humidity": 65
    },
    "dt": 1792150000
}

is_valid, errors = validate_weather(valid_weather)

print("Valid data test:", is_valid)
print("Errors:", errors)


invalid_weather = {
    "name": "Pune",
    "main": {
        "temp": 29.5,
        "humidity": 150
    },
    "dt": 1792150000
}

is_valid, errors = validate_weather(invalid_weather)

print("\nInvalid data test:", is_valid)
print("Errors:", errors)