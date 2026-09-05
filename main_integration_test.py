from ring1_perception import get_perception_output
from ring2_plausibility import check_plausibility
from ring3_arbiter import arbitrate, reset_state

# Simulated drive cycle: a sequence of confidence values over time (frames)
drive_cycle = [0.91, 0.88, 0.20, 0.15, 0.85]

def run_pipeline():
    reset_state()

    for frame_number, confidence in enumerate(drive_cycle, start=1):
        detection = get_perception_output(confidence=confidence)
        is_plausible, reason = check_plausibility(detection)
        status, action_data = arbitrate(detection, is_plausible)

        print(f"Frame {frame_number}: confidence={confidence} -> "
              f"Ring2: {is_plausible} ({reason}) -> Ring3: {status}")

if __name__ == "__main__":
    run_pipeline()