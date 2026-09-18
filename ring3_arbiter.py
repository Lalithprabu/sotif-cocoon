# Ring 3: Safe-State Arbiter - decides vehicle action based on Ring 2's verdict
#
# Uses a temporal trust score (with hysteresis) rather than instant 
# good/bad switching, so recovery from a fault requires sustained good 
# detections, not just one lucky frame. This mirrors debounce/hysteresis 
# techniques used in automotive sensor signal processing.

last_known_good_state = None
trust_score = 0

MAX_TRUST = 5
RECOVERY_THRESHOLD = 3
TRUST_GAIN_ON_GOOD = 1
TRUST_LOSS_ON_BAD = 2


def arbitrate(detection, is_plausible):
    global last_known_good_state, trust_score

    if is_plausible:
        trust_score = min(trust_score + TRUST_GAIN_ON_GOOD, MAX_TRUST)
    else:
        trust_score = max(trust_score - TRUST_LOSS_ON_BAD, 0)

    if trust_score >= RECOVERY_THRESHOLD:
        last_known_good_state = detection
        return "NORMAL_OPERATION", detection

    if last_known_good_state is not None:
        return "DEGRADED_HOLD_LAST_GOOD", last_known_good_state

    return "SAFE_STOP_REQUEST_TAKEOVER", None


def reset_state():
    global last_known_good_state, trust_score
    last_known_good_state = None
    trust_score = 0