from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import ParkingEvent, ParkingSnapshot, PlaceStatus


def get_or_create_place_status(db: Session, camera_id: str, place_id: int) -> PlaceStatus:
    row = db.query(PlaceStatus).filter_by(camera_id=camera_id, place_id=place_id).first()
    if row:
        return row
    row = PlaceStatus(camera_id=camera_id, place_id=place_id, status="free")
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def add_event(db: Session, camera_id: str, place_id: int, old_status: str, new_status: str) -> ParkingEvent:
    event = ParkingEvent(
        camera_id=camera_id,
        place_id=place_id,
        old_status=old_status,
        new_status=new_status,
    )
    db.add(event)
    return event


def add_snapshot(db: Session, camera_id: str, total: int, occupied: int, free: int) -> ParkingSnapshot:
    snap = ParkingSnapshot(camera_id=camera_id, total_places=total, occupied=occupied, free=free)
    db.add(snap)
    return snap


def list_snapshots(db: Session, camera_id: str, limit: int = 50):
    return (
        db.query(ParkingSnapshot)
        .filter_by(camera_id=camera_id)
        .order_by(ParkingSnapshot.created_at.desc())
        .limit(limit)
        .all()
    )


def list_events(db: Session, camera_id: str, limit: int = 50):
    return (
        db.query(ParkingEvent)
        .filter_by(camera_id=camera_id)
        .order_by(ParkingEvent.created_at.desc())
        .limit(limit)
        .all()
    )


def reset_camera_state(db: Session, camera_id: str) -> None:
    db.query(PlaceStatus).filter_by(camera_id=camera_id).delete()
    db.commit()
