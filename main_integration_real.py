from ring1_perception_real import get_real_perception_output
from ring2_plausibility import check_plausibility, reset_state as reset_ring2_state
from ring3_arbiter import arbitrate, reset_state as reset_ring3_state
from logger_config import logger

def run_real_pipeline(image_path):
    reset_ring2_state()
    reset_ring3_state()

    detection = get_real_perception_output(image_path)

    if detection is None:
        message = f"No objects detected in {image_path}"
        logger.warning(message)
        print(message)
        return

    is_plausible, reason = check_plausibility(detection)
    status, action_data = arbitrate(detection, is_plausible)

    message = (f"Image: {image_path} -> Detection: {detection} -> "
               f"Ring2: {is_plausible} ({reason}) -> Ring3: {status}")

    if status == "NORMAL_OPERATION":
        logger.info(message)
    else:
        logger.warning(message)

    print(message)

if __name__ == "__main__":
    run_real_pipeline("images/bus_degraded.jpg")