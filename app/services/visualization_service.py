from pathlib import Path
import cv2
import numpy as np
from app.schemas import Detection, ParkingConfig, ParkingStatusOut
from app.settings import settings


def draw_visualization(
    image: np.ndarray,
    config: ParkingConfig,
    detections: list[Detection],
    status: ParkingStatusOut,
) -> Path:
    output = image.copy()
    status_by_place = {p.place_id: p.status for p in status.places}

    for place in config.places:
        polygon = np.array(place.polygon, dtype=np.int32)
        color = (0, 0, 255) if status_by_place.get(place.id) == "occupied" else (0, 180, 0)
        cv2.polylines(output, [polygon], isClosed=True, color=color, thickness=3)
        x, y = polygon[0]
        cv2.putText(output, f"{place.name}: {status_by_place.get(place.id)}", (int(x), int(y) - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    for det in detections:
        x1, y1, x2, y2 = [int(v) for v in det.bbox]
        cv2.rectangle(output, (x1, y1), (x2, y2), (255, 120, 0), 2)
        cv2.putText(output, f"{det.class_name} {det.confidence:.2f}", (x1, max(20, y1 - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 120, 0), 2)

    filename = f"{config.camera_id}_latest.jpg"
    path = settings.output_dir / filename
    cv2.imwrite(str(path), output)
    return path
