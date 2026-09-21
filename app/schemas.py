from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: list[float]


class ParkingPlace(BaseModel):
    id: int
    name: str
    polygon: list[list[float]] = Field(..., description="List of [x, y] points")


class ParkingConfig(BaseModel):
    camera_id: str
    camera_name: str = "Parking camera"
    image_width: int = 1280
    image_height: int = 720
    occupation_seconds: int = 5
    release_seconds: int = 5
    places: list[ParkingPlace]


class PlaceStatusOut(BaseModel):
    place_id: int
    name: str
    status: Literal["free", "occupied"]
    confidence: float | None = None
    updated_at: datetime | None = None


class ParkingStatusOut(BaseModel):
    camera_id: str
    total_places: int
    occupied: int
    free: int
    places: list[PlaceStatusOut]
    visualization_url: str | None = None


class SnapshotOut(BaseModel):
    id: int
    camera_id: str
    total_places: int
    occupied: int
    free: int
    created_at: datetime


class EventOut(BaseModel):
    id: int
    camera_id: str
    place_id: int
    old_status: str
    new_status: str
    created_at: datetime


class CameraOut(BaseModel):
    camera_id: str
    camera_name: str
    places_count: int
