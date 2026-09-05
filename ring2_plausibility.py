# Ring 2: Plausibility Monitor - checks if Ring 1's output makes physical sense

def check_plausibility(detection):
    confidence_threshold = 0.5
    max_valid_distance_m = 200

    if detection["confidence"] < confidence_threshold:
        return False, "Confidence too low"

    if detection["distance_m"] < 0 or detection["distance_m"] > max_valid_distance_m:
        return False, "Distance out of valid range"

    return True, "Plausible"
if __name__ == "__main__":
    test_detection = {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.91}
    result, reason = check_plausibility(test_detection)
    print(result, "-", reason)