import json
from pathlib import Path
from datetime import datetime

def save_rejected_data(data,city,error):
    """
    Save an  invalid weather record and its validation errors.
    """

    rejected_dir=Path("data/rejected")
    rejected_dir.mkdir(parents=True,exist_ok=True)

    timestamp=datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
    filename=f"{city}_{timestamp}_rejected.json"
    filepath=rejected_dir/filename

    rejection_record={
        "city_rejected":city,
        "rejected_at":datetime.now().isoformat(),
        "validation_errors":error,
        "original_data":data
    }

    with filepath.open("w",encoding="utf-8") as file:
        json.dump(rejection_record,file,indent=4)

    return filepath


