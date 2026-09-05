# Ring 1: Perception Core (currently a STUB - fake AI output for testing)
"""
def get_perception_output():
    detection = {
        "object": "pedestrian",
        "distance_m": 12.5,
        "confidence": 0.2
    }
    return detection
if __name__ == "__main__":
    print(get_perception_output())"""

# Ring 1: Perception Core (currently a STUB - fake AI output for testing)

def get_perception_output(confidence=0.91, distance_m=12.5):
    detection = {
        "object": "pedestrian",
        "distance_m": distance_m,
        "confidence": confidence
    }
    return detection

if __name__ == "__main__":
    print(get_perception_output())