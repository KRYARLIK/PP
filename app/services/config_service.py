import json
from pathlib import Path
from app.schemas import ParkingConfig
from app.settings import settings


def config_path(camera_id: str) -> Path:
    return settings.config_dir / f"{camera_id}.json"


def load_config(camera_id: str) -> ParkingConfig:
    path = config_path(camera_id)
    if not path.exists():
        raise FileNotFoundError(f"Config for camera_id={camera_id} not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return ParkingConfig.model_validate(json.load(f))


def save_config(config: ParkingConfig) -> ParkingConfig:
    settings.config_dir.mkdir(parents=True, exist_ok=True)
    path = config_path(config.camera_id)
    with path.open("w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, ensure_ascii=False, indent=2)
    return config


def list_cameras() -> list[ParkingConfig]:
    settings.config_dir.mkdir(parents=True, exist_ok=True)
    result: list[ParkingConfig] = []
    for path in settings.config_dir.glob("*.json"):
        with path.open("r", encoding="utf-8") as f:
            result.append(ParkingConfig.model_validate(json.load(f)))
    return result
