from functools import lru_cache
import cv2
import numpy as np
from ultralytics import YOLO
from app.settings import settings
from app.schemas import Detection


@lru_cache(maxsize=1)
def get_model() -> YOLO:
    return YOLO(settings.model_path)


def decode_image(file_bytes: bytes) -> np.ndarray:
    array = np.frombuffer(file_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Cannot decode image. Use jpg/png image file.")
    return image


def detect_vehicles(image: np.ndarray) -> list[Detection]:
    model = get_model()
    results = model.predict(image, conf=settings.confidence_threshold, verbose=False)
    detections: list[Detection] = []

    for result in results:
        if result.boxes is None:
            continue
        for box_obj in result.boxes:
            cls_id = int(box_obj.cls[0].item())
            class_name = model.names.get(cls_id, str(cls_id))
            if class_name not in settings.vehicle_classes:
                continue
            confidence = float(box_obj.conf[0].item())
            bbox = [float(v) for v in box_obj.xyxy[0].tolist()]
            detections.append(Detection(class_name=class_name, confidence=confidence, bbox=bbox))

    return detections
