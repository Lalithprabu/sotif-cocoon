# Creates an annotated demo video showing YOLO detections alongside 
# our Cocoon's Ring2/Ring3 safety verdict, overlaid directly on each frame.

import cv2
import glob
from ultralytics import YOLO
from ring2_plausibility import check_plausibility, reset_state as reset_ring2_state
from ring3_arbiter import arbitrate, reset_state as reset_ring3_state

model = YOLO("yolov8n.pt")

reset_ring2_state()
reset_ring3_state()

frame_paths = sorted(glob.glob("images/video_frames/*.jpg"))
annotated_frames = []

for frame_number, frame_path in enumerate(frame_paths, start=1):
    results = model(frame_path, verbose=False)
    plotted_frame = results[0].plot()  # draws YOLO's own boxes/labels

    boxes = results[0].boxes
    if len(boxes) > 0:
        box = boxes[0]
        class_name = model.names[int(box.cls[0])]
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0]
        box_height_pixels = float(y2 - y1)
        distance_m = round(2000 / box_height_pixels, 2)

        detection = {"object": class_name, "distance_m": distance_m, "confidence": round(confidence, 2)}
        is_plausible, reason = check_plausibility(detection)
        status, _ = arbitrate(detection, is_plausible)
    else:
        status = "NO_DETECTION"

    # Overlay our Cocoon's verdict as text on the frame
    color = (0, 255, 0) if status == "NORMAL_OPERATION" else (0, 0, 255)
    cv2.putText(plotted_frame, f"Frame {frame_number}: {status}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    annotated_frames.append(plotted_frame)

# Write annotated frames out as a video
height, width, _ = annotated_frames[0].shape
out = cv2.VideoWriter("images/cocoon_demo.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 2, (width, height))
for frame in annotated_frames:
    out.write(frame)
out.release()

print(f"Saved annotated demo video with {len(annotated_frames)} frames to images/cocoon_demo.mp4")