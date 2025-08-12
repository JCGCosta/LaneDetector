import cv2
import json

import numpy as np

from Source.Utils import import_function_from_file
from Source.Controls import Controls
from Source.PipelineSchema import is_pipeline_valid

class LaneDetector:
    def __init__(self, pipeline: str | dict, controls: bool = False):
        self.RECORD = None
        self.LAST_POLYGON = None
        self.RESOLUTION = None
        self.FRAME_COUNTER = 0
        self.HAS_CONTROLS = controls
        if isinstance(pipeline, str):
            self.PIPELINE = json.loads(open(pipeline).read())
        else:
            self.PIPELINE = pipeline
        if not is_pipeline_valid(self.PIPELINE):
            raise ValueError("Invalid pipeline schema.")
        if self.HAS_CONTROLS:
            self._controls = Controls(self.PIPELINE)
        for op, p in self.PIPELINE.items():
            self.PIPELINE[op]["func"] = import_function_from_file(filepath=p["path"], function_name=p["function"])

    def setup_record(self, resolution: tuple, output_path: str = "output.avi", record_fps: int = 30):
        self.RECORD = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), record_fps, frameSize=resolution)

    def stop_recording(self):
        if self.RECORD is not None:
            self.RECORD.release()
            self.RECORD = None
        else:
            print("Recording is not active, nothing to stop.")

    def update_parameters(self, new_parameters: dict):
        for op, parameters in new_parameters.items():
            self.PIPELINE[op]["parameters"] = parameters

    def frame_processor(self, image: cv2.Mat, frame_skip: int = 0, alpha: float = 1.0, beta: float = 0.5):
        cur_image = np.copy(image)
        if self.FRAME_COUNTER == frame_skip:
            if self.HAS_CONTROLS: self.update_parameters(new_parameters=self._controls.get_values())
            self.FRAME_COUNTER = 0
            for op, param in self.PIPELINE.items():
                cur_image = param["func"](cur_image, param["parameters"])
            if cur_image.any(): self.LAST_POLYGON = np.copy(cur_image)
        else:
            self.FRAME_COUNTER += 1
        if self.LAST_POLYGON is not None:
            image = cv2.addWeighted(image, alpha, self.LAST_POLYGON, beta, 0.0)
        if self.RECORD is not None:
            self.RECORD.write(image)
        return image