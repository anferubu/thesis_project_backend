import re
from typing import Any



def remove_whitespaces(values:Any) -> Any:
    """Remove whitespaces at beginning and end of a string."""

    for key, value in values.items():
        if isinstance(value, str):
            values[key] = value.strip()
    return values



def check_start_end_dates(values:Any) -> Any:
    """Validates that start_date is a date before end_date."""

    start_date = values.get("start_date")
    end_date = values.get("end_date")
    if start_date and end_date and start_date > end_date:
        raise ValueError("Start date must be before or equal to end date.")
    return values



def check_telephone(values:Any, field_name:str) -> Any:
    """Validates that telephone has a valid format."""

    telephone = values.get(field_name)
    if telephone is None: return values
    # remove '-' and spaces from the telephone
    telephone = re.sub(r'[^\d]', '', telephone)
    if telephone and not re.match(r'^3\d{9}$', telephone):
        raise ValueError(
            "Phone number must be a valid mobile number, e.g., 3001234567."
        )
    values[field_name] = telephone
    return values



def check_password(values:Any, field_name:str) -> Any:
    """Validates that the password is secure."""

    password = values.get(field_name)
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\"<>,.?/~`"
    if password.startswith(" ") or password.endswith(" "):
        raise ValueError("Password cannot start or end with spaces.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    if not any(char.islower() for char in password):
        raise ValueError("Password must have a lowercase character.")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must have an uppercase character.")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must have a numeric character.")
    if not any(char in special_characters for char in password):
        raise ValueError("Password must have a special character.")
    return values
