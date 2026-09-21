from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repository import list_events, list_snapshots, reset_camera_state
from app.schemas import CameraOut, EventOut, ParkingConfig, ParkingStatusOut, SnapshotOut
from app.services.config_service import list_cameras, load_config, save_config
from app.services.parking_service import calculate_status
from app.services.video_service import process_video
from app.services.visualization_service import draw_visualization
from app.services.yolo_service import decode_image, detect_vehicles

router = APIRouter(prefix="/api", tags=["parking"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/cameras", response_model=list[CameraOut])
def get_cameras():
    return [
        CameraOut(camera_id=c.camera_id, camera_name=c.camera_name, places_count=len(c.places))
        for c in list_cameras()
    ]


@router.get("/config/{camera_id}", response_model=ParkingConfig)
def get_config(camera_id: str):
    try:
        return load_config(camera_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/config/{camera_id}", response_model=ParkingConfig)
def update_config(camera_id: str, config: ParkingConfig):
    if config.camera_id != camera_id:
        raise HTTPException(status_code=400, detail="camera_id in URL and body must be equal")
    return save_config(config)


@router.post("/detect/image", response_model=ParkingStatusOut)
async def detect_image(
    camera_id: str = Form("parking_1"),
    force: bool = Form(False),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        config = load_config(camera_id)
        image = decode_image(await file.read())
        detections = detect_vehicles(image)
        status = calculate_status(config, detections, db, force=force)
        out_path = draw_visualization(image, config, detections, status)
        status.visualization_url = f"/output/{out_path.name}"
        return status
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/detect/video", response_model=ParkingStatusOut)
async def detect_video(
    camera_id: str = Form("parking_1"),
    every_n_frames: int = Form(10),
    force: bool = Form(False),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        config = load_config(camera_id)
        suffix = Path(file.filename or "video.mp4").suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(await file.read())
            temp_path = Path(temp.name)
        try:
            return process_video(temp_path, config, db, every_n_frames=every_n_frames, force=force)
        finally:
            temp_path.unlink(missing_ok=True)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/parking/{camera_id}/status", response_model=ParkingStatusOut)
def get_status(camera_id: str, db: Session = Depends(get_db)):
    try:
        config = load_config(camera_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    places = []
    from app.db.repository import get_or_create_place_status
    for place in config.places:
        state = get_or_create_place_status(db, camera_id, place.id)
        places.append({
            "place_id": place.id,
            "name": place.name,
            "status": state.status,
            "confidence": state.confidence,
            "updated_at": state.updated_at,
        })
    occupied = sum(1 for p in places if p["status"] == "occupied")
    return ParkingStatusOut(
        camera_id=camera_id,
        total_places=len(places),
        occupied=occupied,
        free=len(places) - occupied,
        places=places,
        visualization_url=f"/output/{camera_id}_latest.jpg",
    )


@router.get("/parking/{camera_id}/history", response_model=list[SnapshotOut])
def get_history(camera_id: str, limit: int = 50, db: Session = Depends(get_db)):
    return list_snapshots(db, camera_id, limit=limit)


@router.get("/parking/{camera_id}/events", response_model=list[EventOut])
def get_events(camera_id: str, limit: int = 50, db: Session = Depends(get_db)):
    return list_events(db, camera_id, limit=limit)


@router.delete("/parking/{camera_id}/state")
def reset_state(camera_id: str, db: Session = Depends(get_db)):
    reset_camera_state(db, camera_id)
    return {"status": "reset", "camera_id": camera_id}
