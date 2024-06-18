"""
Defines the global exception handlers for the app.

It includes:
  - validation_exception_handler(): defines error messages for Pydantic schema
      validations.

"""

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse



async def validation_exception_handler(request, exc:RequestValidationError):
    """
    Handle Pydantic validation errors and return a custom error response. This
    defines the structure of the error message as follows:

    {
        "detail": "There was an error validating your input.",
        "errors": [
            {
                "type": "type_error.integer",
                "field": "age (bad input: twenty-five)",
                "description": "value is not a valid integer"
            }
        ]
    }
    """

    errors = exc.errors()
    response = {
        "detail": "There was an error validating your input.",
        "errors": []
    }

    for error in errors:
        error_type = error["type"]
        description = error["msg"]
        loc_value = error["loc"][1]

        if error_type == "json_invalid":
            res = {
                "type": error_type,
                "description": description
            }

        else:
            field_info = f"{loc_value} (bad input: {error['input']})"

            res = {
                "type": error_type,
                "field": field_info,
                "description": description
            }

        response["errors"].append(res)

    return JSONResponse(response, status_code=400)