from enum import Enum
from datetime import date


def get_type_error_message(variable_name: str, expected_type, variable_value) -> str:
    return f"{variable_name} must be {expected_type}, got {variable_value} of type {type(variable_value).__name__}"


def get_enum_error_message(variable_name: str, enum: Enum, variable_value) -> str:
    return f"{variable_name} must be one of {', '.join([e.value for e in enum])}, got {variable_value}"


def get_enum_date_must_be_before_or_equal(
    variable_name: str,
    variable_value: date,
    after_variable_name: str,
    after_variable_value: date,
):
    return f"{variable_name} {variable_value} must be before or equal to {after_variable_name} {after_variable_value}"


def get_enum_date_must_be_after_or_equal(
    variable_name: str,
    variable_value: date,
    after_variable_name: str,
    after_variable_value: date,
):
    return f"{variable_name} {variable_value} must be after or equal to {after_variable_name} {after_variable_value}"

def get_invalid_postal_code_message(postal_code: str) -> str:
    return f"Invalid Canadian postal code '{postal_code}'. It should follow the format 'ANA NAN', where A is a letter and N is a digit."
