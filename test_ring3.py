from ring2_plausibility import check_plausibility, reset_state as reset_ring2_state
from ring3_arbiter import arbitrate, reset_state as reset_ring3_state

sequence_test_cases = [
    {
        "name": "Single frame - good detection",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.91},
             "expected_status": "NORMAL_OPERATION"}
        ]
    },
    {
        "name": "Single frame - bad confidence, no history",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.2},
             "expected_status": "SAFE_STOP_REQUEST_TAKEOVER"}
        ]
    },
    {
        "name": "Single frame - bad distance (negative), no history",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": -5, "confidence": 0.91},
             "expected_status": "SAFE_STOP_REQUEST_TAKEOVER"}
        ]
    },
    {
        "name": "Single frame - bad distance (too far), no history",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": 250, "confidence": 0.91},
             "expected_status": "SAFE_STOP_REQUEST_TAKEOVER"}
        ]
    },
    {
        "name": "Good then bad confidence - should hold last good state",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.91},
             "expected_status": "NORMAL_OPERATION"},
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.2},
             "expected_status": "DEGRADED_HOLD_LAST_GOOD"}
        ]
    }
]

def run_tests():
    for case in sequence_test_cases:
        reset_ring2_state()
        reset_ring3_state()
        print(f"--- {case['name']} ---")
        for i, frame in enumerate(case["frames"], start=1):
            is_plausible, reason = check_plausibility(frame["detection"])
            status, action_data = arbitrate(frame["detection"], is_plausible)
            passed = status == frame["expected_status"]
            result = "PASS" if passed else "FAIL"
            print(f"  [{result}] Frame {i}: expected {frame['expected_status']}, "
                  f"got {status} (Ring2: {reason})")

if __name__ == "__main__":
    run_tests()