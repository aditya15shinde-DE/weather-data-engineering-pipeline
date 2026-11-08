from unittest.mock import patch
from pathlib import Path
import json

import main


def test_pipeline_rejection():

    sample_invalid_weather = {
        "name": "TestCity",
        "dt": 1792150000,
        "main": {
            "temp": 28.5,
            "humidity": 150
        }
    }

    rejected_dir = Path("data/rejected")
    rejected_dir.mkdir(parents=True, exist_ok=True)

    existing_files = set(
        rejected_dir.glob("TestCity_*_rejected.json")
    )

    with patch.object(main, "CITIES", ["TestCity"]):

        with patch.object(
            main,
            "get_weather",
            return_value=sample_invalid_weather
        ):

            with patch.object(main, "save_raw_data"):

                main.main()

    new_files = (
        set(rejected_dir.glob("TestCity_*_rejected.json"))
        - existing_files
    )

    assert new_files, "FAIL: No new rejected-data file was created."

    latest_file = max(
        new_files,
        key=lambda file: file.stat().st_mtime
    )

    with latest_file.open("r", encoding="utf-8") as file:
        rejected_record = json.load(file)

    assert rejected_record["city_rejected"] == "TestCity"

    assert "Humidity must be between 0 and 100" in (
        rejected_record["validation_errors"]
    )

    print("\nPASS: The main pipeline saved the invalid record.")
    print(f"Rejected file: {latest_file}")
    print("Validation errors:", rejected_record["validation_errors"])


if __name__ == "__main__":
    test_pipeline_rejection()