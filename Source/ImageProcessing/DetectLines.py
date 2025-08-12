import cv2
import numpy as np

def draw_polygon(image: cv2.Mat, params: dict):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lines = lane_lines(
        gray,
        cv2.HoughLinesP(
          gray,
          rho=params["rho"][0],
          theta=np.pi / params["theta"][0],
          threshold=params["threshold"][0],
          minLineLength=params["min_line_length"][0],
          maxLineGap=params["max_line_gap"][0]
        ),
        params['detect_dist'][0],
    )
    return draw_lane_polygon(
        gray,
        lines,
        color=[
            params['polygon_color_B'][0],
            params['polygon_color_G'][0],
            params['polygon_color_R'][0]
        ]
    )

def draw_lane_polygon(image: cv2.Mat, lines, color: tuple):
    if color is None:
        color = [255, 0, 0]
    polygon_image = cv2.cvtColor(np.zeros_like(image), cv2.COLOR_GRAY2RGB)
    if not None in lines:
        points = np.array([lines[0][0], lines[1][0], lines[1][1], lines[0][1]])
        cv2.fillPoly(polygon_image, np.int32([points]), color)
    return polygon_image

def average_slope_intercept(lines):
    left_lines = []  # (slope, intercept)
    left_weights = []  # (length,)
    right_lines = []  # (slope, intercept)
    right_weights = []  # (length,)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == x2:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - (slope * x1)
                length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
                if slope < 0:
                    left_lines.append((slope, intercept))
                    left_weights.append(length)
                else:
                    right_lines.append((slope, intercept))
                    right_weights.append(length)
        left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if len(left_weights) > 0 else None
        right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
        return left_lane, right_lane
    else:
        return None, None

def pixel_points(y1, y2, line):
    if line is None:
        return None
    slope, intercept = line
    try:
        return (int((y1 - intercept) / slope), int(y1)), (int((y2 - intercept) / slope), int(y2))
    except OverflowError:
        return None

def lane_lines(image, lines, detect_dist):
    left_lane, right_lane = average_slope_intercept(lines)
    y1 = image.shape[0]
    y2 = y1 * ((100 - detect_dist) * 0.01)
    left_line = pixel_points(y1, y2, left_lane)
    right_line = pixel_points(y1, y2, right_lane)
    return left_line, right_line