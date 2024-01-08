from jsonschema import validate, ValidationError

employee_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "dob": {"type": "string", "format": "date"},
        "date_joined": {"type": "string", "format": "date"},
        "date_left": {"anyOf": [{"type": "string", "format": "date"}, {"type": "null"}]},
        "identity_no": {"type": "string"},
        "department": {"type": "string", "enum": ["admin", "engineering", "management", "sales", "qc"]},
        "salary": {"anyOf": [{"type": "number"}, {"type": "integer"}]},
        "remark": {"type": "string"}
    },
    "required": ["name", "dob", "date_joined", "identity_no", "department", "salary", "remark"]
}


def validate_employee(data):
    try:
        validate(data, employee_schema)

        # Additional validation for date_joined and date_left
        date_joined = data.get("date_joined")
        date_left = data.get("date_left")

        if date_joined and date_left and date_left < date_joined:
            raise ValidationError("date_left must be later than date_joined")

        return None  # Validation successful
    except ValidationError as e:
        return str(e)

# def validate_employee(data):
#     try:
#         validate(data, employee_schema)
#         return None  # Validation successful
#     except ValidationError as e:
#         return str(e)