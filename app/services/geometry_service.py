from shapely.geometry import Point, Polygon, box


def bbox_to_polygon(bbox: list[float]) -> Polygon:
    x1, y1, x2, y2 = bbox
    return box(x1, y1, x2, y2)


def point_inside_polygon(point: tuple[float, float], polygon_points: list[list[float]]) -> bool:
    return Polygon(polygon_points).contains(Point(point))


def bbox_center(bbox: list[float]) -> tuple[float, float]:
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def intersection_ratio(place_polygon: list[list[float]], bbox: list[float]) -> float:
    place = Polygon(place_polygon)
    vehicle = bbox_to_polygon(bbox)
    if place.area <= 0:
        return 0.0
    intersection_area = place.intersection(vehicle).area
    return float(intersection_area / place.area)
