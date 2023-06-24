from enum import Enum
def get_type_error_message(variable_name: str, expected_type, variable_value) -> str:
    return f"{variable_name} must be {expected_type}, got {variable_value} of type {type(variable_value).__name__}"

def get_enum_error_message(variable_name: str, enum:Enum, variable_value) -> str:
    return f"{variable_name} must be one of {', '.join([e.value for e in enum])}, got {variable_value}"