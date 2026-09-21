import json
from pathlib import Path

config = {
    "camera_id": "parking_2",
    "camera_name": "Second parking camera",
    "image_width": 1280,
    "image_height": 720,
    "occupation_seconds": 5,
    "release_seconds": 5,
    "places": [
        {"id": 1, "name": "B1", "polygon": [[100, 250], [220, 250], [230, 380], [90, 380]]},
        {"id": 2, "name": "B2", "polygon": [[240, 250], [360, 250], [370, 380], [230, 380]]},
    ],
}
Path("configs").mkdir(exist_ok=True)
Path("configs/parking_2.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
print("Created configs/parking_2.json")
