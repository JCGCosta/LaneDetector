import cv2
import numpy as np

def apply_masks_protocol(image: cv2.Mat, params: dict):
    # White color mask
    white_mask = cv2.inRange(
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
        np.uint8([params["white_mask_lower_threshold"][0]]), np.uint8([255])
    )
    # Yellow color mask
    yellow_mask = cv2.inRange(
        cv2.cvtColor(image, cv2.COLOR_BGR2HLS),
        np.uint8([10, 0, 100]), np.uint8([40, 255, 255])
    )
    # Combine white and yellow masks
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    return cv2.bitwise_and(image, image, mask=mask)