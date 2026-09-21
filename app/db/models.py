from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class PlaceStatus(Base):
    __tablename__ = "place_statuses"
    __table_args__ = (UniqueConstraint("camera_id", "place_id", name="uq_camera_place"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String, index=True)
    place_id: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String, default="free")
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    occupied_candidate_since: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    free_candidate_since: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ParkingSnapshot(Base):
    __tablename__ = "parking_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String, index=True)
    total_places: Mapped[int] = mapped_column(Integer)
    occupied: Mapped[int] = mapped_column(Integer)
    free: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class ParkingEvent(Base):
    __tablename__ = "parking_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String, index=True)
    place_id: Mapped[int] = mapped_column(Integer, index=True)
    old_status: Mapped[str] = mapped_column(String)
    new_status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
