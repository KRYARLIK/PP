from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = "Parking YOLO Backend"
    model_path: str = "yolo11n.pt"
    vehicle_classes: set[str] = {"car", "truck", "bus", "motorcycle"}
    confidence_threshold: float = 0.35
    intersection_threshold: float = 0.20
    database_url: str = "postgresql+psycopg2://parking_user:parking_password@localhost:5432/parking_db"
    config_dir: Path = Path("configs")
    output_dir: Path = Path("data/output")


settings = Settings()
settings.output_dir.mkdir(parents=True, exist_ok=True)
