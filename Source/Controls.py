import json

import dearpygui.dearpygui as dpg
import threading

class Controls:
    def __init__(self, pipeline_obj: dict, window_name: str = "Controls", controls_res: tuple = (800, 700)):
        self.cur_pipeline = pipeline_obj
        self.window_name = window_name
        self.window_width, self.window_height = controls_res
        self.parameters = self._extract_parameters()
        self.cur_values = {}  # Current slider values (int only)
        self.cur_op = {k: True for k in self.cur_pipeline.keys()}
        self.shutdown = False
        self._setup_controls()

    def _extract_parameters(self) -> dict:
        parameters = {}
        for op, param in self.cur_pipeline.items():
            for k, v in param["parameters"].items():
                parameters.setdefault(op, {})[k] = v
        return parameters

    def _update_operations(self, sender, app_data):
        op, _ = sender.split(".")
        self.cur_op[op] = app_data

    def _update_value(self, sender, app_data):
        op, param_name = sender.split(".")
        self.cur_values[op][param_name][0] = app_data

    def _setup_controls(self):
        dpg.create_context()
        with dpg.window(label=self.window_name, width=self.window_width, height=self.window_height):
            for op, parameters in self.parameters.items():
                with dpg.collapsing_header(label=op, default_open=True):
                    self.cur_values[op] = {}
                    dpg.add_checkbox(
                        label="Enable",
                        default_value=True,
                        callback=self._update_operations,
                        tag=op + ".enable",
                    )
                    for param_name, param_value in parameters.items():
                        field_name = f"{op}.{param_name}"

                        if len(param_value) == 2:
                            init_val, max_val = param_value
                            if isinstance(init_val, list):
                                init_val = init_val[0]
                        else:
                            print(f"Skipping {field_name}: invalid format {param_value}")
                            continue

                        self.cur_values[op][param_name] = [int(init_val), int(max_val)]

                        dpg.add_slider_int(
                            label=param_name,
                            default_value=int(init_val),
                            max_value=int(max_val),
                            callback=self._update_value,
                            tag=field_name
                        )

    def get_values(self):
        return self.cur_values

    def get_ops(self):
        return self.cur_op

    def _shutdown(self):
        self.shutdown = True

    def display_controls(self):
        def gui_thread():
            dpg.destroy_context()
            dpg.create_context()
            self._setup_controls()
            dpg.create_viewport(title=self.window_name, width=self.window_width, height=self.window_height)
            dpg.set_exit_callback(self._shutdown)
            dpg.setup_dearpygui()
            dpg.show_viewport()
            dpg.start_dearpygui()
            dpg.destroy_context()

        thread = threading.Thread(target=gui_thread, daemon=True)
        thread.start()
        return thread

if __name__ == "__main__":
    with open("../pipeline.json") as f:
        pipeline = json.load(f)

    dpg.create_context()

    controls = Controls(pipeline_obj=pipeline)
    print("Controls initialized. Adjust the sliders in the DearPyGui window.")
    controls.display_controls()