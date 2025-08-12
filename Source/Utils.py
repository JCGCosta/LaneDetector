import importlib.util
import sys
import os
import cv2

def get_video_resolution(cap: cv2.VideoCapture) -> tuple:
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video file: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return tuple([width, height])

def import_function_from_file(filepath, function_name):
    # Check if file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    module_name = os.path.splitext(os.path.basename(filepath))[0]

    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None:
            raise ImportError(f"Could not load module spec from {filepath}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Failed to load module '{module_name}': {e}")

    # Check if function exists
    if not hasattr(module, function_name):
        raise AttributeError(f"Function '{function_name}' not found in '{filepath}'")

    func = getattr(module, function_name)
    if not callable(func):
        raise TypeError(f"'{function_name}' in '{filepath}' is not a callable function")

    return func