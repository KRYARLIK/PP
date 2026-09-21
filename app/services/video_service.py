from pathlib import Path
import cv2
from sqlalchemy.orm import Session
from app.schemas import ParkingConfig, ParkingStatusOut
from app.services.parking_service import calculate_status
from app.services.visualization_service import draw_visualization
from app.services.yolo_service import detect_vehicles


def process_video(path: Path, config: ParkingConfig, db: Session, every_n_frames: int = 10, force: bool = False) -> ParkingStatusOut:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    last_status: ParkingStatusOut | None = None
    frame_idx = 0
    last_frame = None
    last_detections = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_idx % every_n_frames == 0:
            last_detections = detect_vehicles(frame)
            last_status = calculate_status(config, last_detections, db, force=force)
            last_frame = frame
        frame_idx += 1

    cap.release()
    if last_status is None or last_frame is None:
        raise ValueError("Video has no readable frames")

    out_path = draw_visualization(last_frame, config, last_detections, last_status)
    last_status.visualization_url = f"/output/{out_path.name}"
    return last_status
