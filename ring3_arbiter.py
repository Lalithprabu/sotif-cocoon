# Ring 3: Safe-State Arbiter - decides vehicle action based on Ring 2's verdict

last_known_good_state = None

def arbitrate(detection, is_plausible):
    global last_known_good_state

    if is_plausible:
        last_known_good_state = detection
        return "NORMAL_OPERATION", detection

    if last_known_good_state is not None:
        return "DEGRADED_HOLD_LAST_GOOD", last_known_good_state

    return "SAFE_STOP_REQUEST_TAKEOVER", None


def reset_state():
    global last_known_good_state
    last_known_good_state = None
    
if __name__ == "__main__":
    good = {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.91}
    bad = {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.2}

    print(arbitrate(good, True))
    print(arbitrate(bad, False))