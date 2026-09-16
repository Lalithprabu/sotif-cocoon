# Ring 1 (REAL): Perception Core using a genuine pretrained YOLO model.
#
# NOTE: This is a simplified proxy, not a production perception stack.
# Real distance estimation would require camera calibration / depth 
# sensing, which is out of scope here. We approximate "distance" using 
# bounding box size as a rough stand-in, purely to demonstrate the 
# Cocoon's architecture against genuine AI model output.

from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def get_real_perception_output(image_path):
    results = model(image_path, verbose=False)
    boxes = results[0].boxes

    if len(boxes) == 0:
        return None

    box = boxes[0]
    class_id = int(box.cls[0])
    class_name = model.names[class_id]
    confidence = float(box.conf[0])

    x1, y1, x2, y2 = box.xyxy[0]
    box_height_pixels = float(y2 - y1)

    approx_distance_m = 2000 / box_height_pixels

    detection = {
        "object": class_name,
        "distance_m": round(approx_distance_m, 2),
        "confidence": round(confidence, 2)
    }
    return detection

if __name__ == "__main__":
    result = get_real_perception_output("images/bus.jpg")
    print(result)