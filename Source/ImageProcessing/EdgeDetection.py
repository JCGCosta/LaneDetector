import cv2
from warnings import warn

def apply_canny_edge_detection(image: cv2.Mat, params: dict):
    if params["aperture_size"][0] not in [3, 5, 7]:
        warn("aperture size must be 3, 5 or 7, using default value of 3.")
        params["aperture_size"][0] = 3
    edges = cv2.Canny(image, params["threshold1"][0], params["threshold2"][0], apertureSize=params["aperture_size"][0])
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)