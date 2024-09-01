import logging
from typing import List, Dict, Any, Tuple, Union

def validate_data(data: List[Dict[str, Any]], source: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    errors = []
    valid_data = []

    for index, item in enumerate(data):
        item_errors = []

        # Rule 1: Check if all required fields are present
        required_fields = ['customer_id', 'meter_id', 'consumption_value', 'timestamp']
        for field in required_fields:
            if field not in item:
                item_errors.append(f"Missing required field: {field}")

        # Rule 2: Check if consumption_value is a positive number
        if 'consumption_value' in item:
            try:
                consumption = float(item['consumption_value'])
                if consumption <= 0:
                    item_errors.append("consumption_value must be a positive number")
            except ValueError:
                item_errors.append("consumption_value must be a valid number")

        if item_errors:
            errors.extend([f"Item {index}: {error}" for error in item_errors])
        else:
            valid_data.append(item)

    if errors:
        logging.warning(f"Validation errors occurred for {source}. {len(errors)} items failed validation.")
        for error in errors:
            logging.warning(f"Error in {source}: {error}")

    logging.info(f"Successfully validated {len(valid_data)} items from {source}")

    return errors, valid_data