from src.validation.weather_validation import validate_weather
from src.validation.rejected_data import save_rejected_data


sample_rejected_data={
    "name": "TestCity",
    "dt": 1792150000,
    "main": {
        "temp": 28.5,
        "humidity": 150
    }
}

is_valid,errors=validate_weather(sample_rejected_data)

print("Is valid:",is_valid)
print("validation errors",errors)

if not is_valid:
    filepath = save_rejected_data(sample_rejected_data,"TestCity",errors)

    print("rejected file created:",filepath)