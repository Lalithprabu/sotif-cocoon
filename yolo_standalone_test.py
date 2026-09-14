from ultralytics import YOLO
from ultralytics.utils.downloads import safe_download

# Download a standard COCO benchmark test image (industry-standard test asset)
safe_download(url="https://ultralytics.com/images/bus.jpg", dir="images")

model = YOLO("yolov8n.pt")
results = model("images/bus.jpg")
results[0].show()