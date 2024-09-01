INTERNAL_SCHEMA = {
    "type": "object",
    "properties": {
        "customer_id": {"type": "string"},
        "meter_id": {"type": "string"},
        "utility_type": {"type": "string", "enum": ["electricity", "water", "gas"]},
        "consumption_value": {"type": "number"},
        "consumption_unit": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "category": {"type": "string"},
        "additional_info": {
            "type": "object",
            "additionalProperties": True
        }
    }
}