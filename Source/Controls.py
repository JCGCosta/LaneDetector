import cv2
import json

class Controls:
    def __init__(self, pipeline: dict, window_name: str = "Controls"):
        self.cur_pipeline = pipeline
        self.window_name = window_name
        self.parameters = self._extract_parameters()
        self.cur_values = {}  # Current slider values (int only)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        self._setup_controls()

    def _extract_parameters(self) -> dict:
        parameters = {}
        for op, param in self.cur_pipeline.items():
            for k, v in param["parameters"].items():
                if op not in parameters.keys(): parameters[op] = {}
                parameters[op][k] = v
        return parameters

    def _update_value(self, field_name: str):
        def callback(val: int):
            op, param_name = field_name.split(".")
            self.cur_values[op][param_name][0] = val
        return callback

    def _setup_controls(self):
        for op, parameters in self.parameters.items():
            for param_name, param_value in parameters.items():
                field_name = op + "." + param_name
                if len(param_value) == 2:
                    init_val, max_val = param_value[0], param_value[1]
                    if isinstance(init_val, list):
                        init_val = init_val[0]
                else:
                    print(f"Skipping {field_name}: invalid format {param_value}")
                    continue

                # Store only the initial numeric value
                if op not in self.cur_values.keys(): self.cur_values[op] = {}
                self.cur_values[op][param_name] = [int(init_val), int(max_val)]

                cv2.createTrackbar(
                    field_name,
                    self.window_name,
                    int(init_val),
                    int(max_val),
                    self._update_value(field_name)
                )

    def get_values(self):
        return self.cur_values


if __name__ == "__main__":
    with open("../pipeline.json") as f:
        pipeline = json.load(f)

    controls = Controls(pipeline=pipeline)
    print("Controls initialized. Adjust the sliders in the OpenCV window.")

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to exit
            break
        print(controls.get_values())
    cv2.destroyAllWindows()