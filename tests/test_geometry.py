from app.services.geometry_service import bbox_center, intersection_ratio, point_inside_polygon


def test_bbox_center():
    assert bbox_center([0, 0, 10, 20]) == (5, 10)


def test_point_inside_polygon():
    polygon = [[0, 0], [10, 0], [10, 10], [0, 10]]
    assert point_inside_polygon((5, 5), polygon) is True
    assert point_inside_polygon((20, 20), polygon) is False


def test_intersection_ratio():
    polygon = [[0, 0], [10, 0], [10, 10], [0, 10]]
    assert intersection_ratio(polygon, [0, 0, 10, 10]) == 1.0
