import requests

url = "http://127.0.0.1:8000/api/detect/image"
image_path = "data/input/parking.jpg"

with open(image_path, "rb") as f:
    files = {"file": f}
    data = {"camera_id": "parking_1", "force": "true"}
    response = requests.post(url, files=files, data=data, timeout=120)

print(response.status_code)
print(response.json())
