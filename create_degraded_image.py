# Deliberately degrades a clean test image to simulate poor sensing 
# conditions (e.g. fog, low resolution, motion blur) - used to test 
# how the real AI model (and our Cocoon) behaves under uncertainty.

from PIL import Image, ImageFilter

original = Image.open("images/bus.jpg")

# Shrink drastically, then scale back up - destroys fine detail
small = original.resize((40, 30))
degraded = small.resize(original.size)

# Apply blur on top for an additional realism pass
degraded = degraded.filter(ImageFilter.GaussianBlur(radius=3))

degraded.save("images/bus_degraded.jpg")
print("Saved degraded image to images/bus_degraded.jpg")