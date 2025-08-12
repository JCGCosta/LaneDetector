import cv2

def apply_gaussian_blur(image: cv2.Mat, params: dict):
    return cv2.GaussianBlur(image, [params["kernel_size"][0], params["kernel_size"][0]], params["sigma"][0])