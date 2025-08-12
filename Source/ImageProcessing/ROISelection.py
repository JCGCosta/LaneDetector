import cv2
import numpy as np

def _get_rectangle_points(center_x, center_y, slope, width, height):
    # Calculate half the width and height
    half_width = width / 2
    half_height = height / 2
    # Calculate the x-component of the slope angle
    x_component = slope * half_height
    # Calculate the four points of the rectangle
    point1 = (center_x - half_width - x_component, center_y - half_height)
    point2 = (center_x + half_width - x_component, center_y + half_height)
    point3 = (center_x + half_width + x_component, center_y + half_height)
    point4 = (center_x - half_width + x_component, center_y - half_height)
    return point1, point2, point3, point4

def apply_double_region_selection(image: cv2.Mat, params: dict):
    ignore_mask_color = (255,) * image.shape[2]
    rows, cols = image.shape[:2]
    gap_between = params["gap"][0] * (cols / 100)
    center_yb = params["center_y"][0] * (rows / 100)
    real_width = params["width"][0] * (cols / 100)
    real_height = params["height"][0] * (rows / 100)
    real_slope = params["slope"][0] * 0.01
    l_mask = np.zeros_like(image)
    r_mask = np.zeros_like(image)
    cv2.fillPoly(l_mask,
                 np.array([_get_rectangle_points(
                     (params["center_x"][0] * (cols / 100)) - gap_between / 2,
                     center_yb,
                     real_slope,
                     -real_width,
                     real_height)
                 ], dtype=np.int32),
                 ignore_mask_color
                 )
    cv2.fillPoly(r_mask,
                 np.array([_get_rectangle_points(
                     (params["center_x"][0] * (cols / 100)) + gap_between / 2,
                     center_yb,
                     real_slope,
                     real_width,
                     real_height)
                 ], dtype=np.int32),
                 ignore_mask_color
                 )
    masked_image = cv2.bitwise_or(l_mask, r_mask)
    return cv2.bitwise_and(image, masked_image)