from schema import Schema, And, Or
import warnings


# Each parameter value is [min, max] where min/max can be int or float
parameter_range_schema = [Or(int, float), int]

operation_schema = {
    'path': And(str, len),
    'function': And(str, len),
    'parameters': {str: parameter_range_schema}
}

PIPELINE_SCHEMA = Schema({str: operation_schema})

def is_pipeline_valid(pipeline: dict) -> bool:
    if not PIPELINE_SCHEMA.is_valid(pipeline):
        warnings.warn("Pipeline Invalid: Schema validation failed.")
        return False
    return True