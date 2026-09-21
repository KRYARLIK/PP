from datetime import datetime
from sqlalchemy.orm import Session
from app.db import repository
from app.schemas import Detection, ParkingConfig, ParkingStatusOut, PlaceStatusOut
from app.services.geometry_service import intersection_ratio
from app.settings import settings


def _place_detected(place_polygon: list[list[float]], detections: list[Detection]) -> tuple[bool, float | None]:
    best_ratio = 0.0
    best_conf = None
    for det in detections:
        ratio = intersection_ratio(place_polygon, det.bbox)
        if ratio > best_ratio:
            best_ratio = ratio
            best_conf = det.confidence
    return best_ratio >= settings.intersection_threshold, best_conf


def calculate_status(config: ParkingConfig, detections: list[Detection], db: Session, force: bool = False) -> ParkingStatusOut:
    now = datetime.utcnow()
    place_outputs: list[PlaceStatusOut] = []

    for place in config.places:
        detected, conf = _place_detected(place.polygon, detections)
        state = repository.get_or_create_place_status(db, config.camera_id, place.id)
        old_status = state.status

        if force:
            new_status = "occupied" if detected else "free"
            state.occupied_candidate_since = now if detected else None
            state.free_candidate_since = now if not detected else None
        elif detected:
            state.free_candidate_since = None
            if state.status == "occupied":
                new_status = "occupied"
            else:
                if state.occupied_candidate_since is None:
                    state.occupied_candidate_since = now
                elapsed = (now - state.occupied_candidate_since).total_seconds()
                new_status = "occupied" if elapsed >= config.occupation_seconds else state.status
        else:
            state.occupied_candidate_since = None
            if state.status == "free":
                new_status = "free"
            else:
                if state.free_candidate_since is None:
                    state.free_candidate_since = now
                elapsed = (now - state.free_candidate_since).total_seconds()
                new_status = "free" if elapsed >= config.release_seconds else state.status

        if new_status != old_status:
            repository.add_event(db, config.camera_id, place.id, old_status, new_status)

        state.status = new_status
        state.confidence = conf
        state.updated_at = now
        db.add(state)

        place_outputs.append(
            PlaceStatusOut(
                place_id=place.id,
                name=place.name,
                status=state.status,
                confidence=state.confidence,
                updated_at=state.updated_at,
            )
        )

    total = len(place_outputs)
    occupied = sum(1 for p in place_outputs if p.status == "occupied")
    free = total - occupied
    repository.add_snapshot(db, config.camera_id, total, occupied, free)
    db.commit()

    return ParkingStatusOut(
        camera_id=config.camera_id,
        total_places=total,
        occupied=occupied,
        free=free,
        places=place_outputs,
    )
