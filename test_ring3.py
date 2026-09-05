from ring3_arbiter import arbitrate, reset_state

sequence_test_cases = [
    {
        "name": "Single frame - good detection",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.91},
             "is_plausible": True,
             "expected_status": "NORMAL_OPERATION"}
        ]
    },
    {
        "name": "Single frame - bad detection, no history",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.2},
             "is_plausible": False,
             "expected_status": "SAFE_STOP_REQUEST_TAKEOVER"}
        ]
    },
    {
        "name": "Good then bad - should hold last good state",
        "frames": [
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.91},
             "is_plausible": True,
             "expected_status": "NORMAL_OPERATION"},
            {"detection": {"object": "pedestrian", "distance_m": 12.5, "confidence": 0.2},
             "is_plausible": False,
             "expected_status": "DEGRADED_HOLD_LAST_GOOD"}
        ]
    }
]
def run_tests():
    for case in sequence_test_cases:
        reset_state()
        print(f"--- {case['name']} ---")
        for i, frame in enumerate(case["frames"], start=1):
            status, data = arbitrate(frame["detection"], frame["is_plausible"])
            passed = status == frame["expected_status"]
            result = "PASS" if passed else "FAIL"
            print(f"  [{result}] Frame {i}: expected {frame['expected_status']}, got {status}")

if __name__ == "__main__":
    run_tests()