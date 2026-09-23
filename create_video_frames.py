# Extracts individual frames from a short sample video, to feed our 
# real-AI pipeline a genuine sequence of consecutive real-world frames 
# (rather than the same static image repeated).

import cv2
from ultralytics.utils.downloads import safe_download

# Download a standard Ultralytics sample video (reproducible test asset)
#safe_download(url="https://ultralytics.com/assets/decelera_landscape_min.mov", dir="videos")

video_path = "videos/Lavendar_London.mp4"
output_dir = "images/video_frames"

import os
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_count = 0
saved_count = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    # Only save every 10th frame, so we get a manageable number of 
    # meaningfully different frames rather than near-duplicates
    if frame_count % 15 == 0:
        filename = f"{output_dir}/frame_{saved_count:03d}.jpg"
        cv2.imwrite(filename, frame)
        saved_count += 1

    frame_count += 1

cap.release()
print(f"Extracted {saved_count} frames from {frame_count} total frames.")