# Ring 2: Plausibility Monitor - checks if Ring 1's output makes physical sense

last_accepted_distance_m = None

def check_plausibility(detection):
    global last_accepted_distance_m

    confidence_threshold = 0.5
    max_valid_distance_m = 200
    max_distance_jump_m = 5

    if detection["confidence"] < confidence_threshold:
        return False, "Confidence too low"

    if detection["distance_m"] < 0 or detection["distance_m"] > max_valid_distance_m:
        return False, "Distance out of valid range"

    if last_accepted_distance_m is not None:
        jump = abs(detection["distance_m"] - last_accepted_distance_m)
        if jump > max_distance_jump_m:
            return False, f"Implausible distance jump ({jump:.1f}m)"

    last_accepted_distance_m = detection["distance_m"]
    return True, "Plausible"


def reset_state():
    global last_accepted_distance_m
    last_accepted_distance_m = None