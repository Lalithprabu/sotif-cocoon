# Deliberately degrades a contiguous block of real video frames to 
# simulate a transient sensing fault (e.g. motion blur, glare, 
# temporary occlusion) partway through an otherwise clean sequence.

import glob
import os
from PIL import Image, ImageFilter

FAULT_START_FRAME = 20
FAULT_END_FRAME = 29

frame_paths = sorted(glob.glob("images/video_frames/*.jpg"))
output_dir = "images/video_frames_with_fault"
os.makedirs(output_dir, exist_ok=True)

for frame_path in frame_paths:
    filename = os.path.basename(frame_path)
    frame_index = int(filename.replace("frame_", "").replace(".jpg", ""))

    image = Image.open(frame_path)

    if FAULT_START_FRAME <= frame_index <= FAULT_END_FRAME:
        small = image.resize((30, 20))
        image = small.resize(image.size)
        image = image.filter(ImageFilter.GaussianBlur(radius=4))

    image.save(f"{output_dir}/{filename}")

print(f"Wrote {len(frame_paths)} frames to {output_dir}, "
      f"with fault injected in frames {FAULT_START_FRAME}-{FAULT_END_FRAME}")