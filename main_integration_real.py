from ring1_perception_real import get_real_perception_output
from ring2_plausibility import check_plausibility, reset_state as reset_ring2_state
from ring3_arbiter import arbitrate, reset_state as reset_ring3_state
from logger_config import logger

def run_real_pipeline_sequence(image_paths):
    reset_ring2_state()
    reset_ring3_state()

    for frame_number, image_path in enumerate(image_paths, start=1):
        detection = get_real_perception_output(image_path)

        if detection is None:
            message = f"Frame {frame_number} ({image_path}): No objects detected"
            logger.warning(message)
            print(message)
            continue

        is_plausible, reason = check_plausibility(detection)
        status, action_data = arbitrate(detection, is_plausible)

        message = (f"Frame {frame_number} ({image_path}): Detection: {detection} -> "
                   f"Ring2: {is_plausible} ({reason}) -> Ring3: {status}")

        if status == "NORMAL_OPERATION":
            logger.info(message)
        else:
            logger.warning(message)

        print(message)

if __name__ == "__main__":
    sequence = ["images/bus.jpg", "images/bus.jpg", "images/bus.jpg"]
    run_real_pipeline_sequence(sequence)