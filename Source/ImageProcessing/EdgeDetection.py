import cv2

def apply_canny_edge_detection(image: cv2.Mat, params: dict):
    edges = cv2.Canny(image, params["threshold1"][0], params["threshold2"][0], apertureSize=params["aperture_size"][0])
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)