from typing import Dict, List, Any, Union
from datetime import datetime
import logging
from data.schema import INTERNAL_SCHEMA

def parse_date(date_string: str) -> str:
    date_formats = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt).isoformat()
        except ValueError:
            continue
    logging.warning(f"Unable to parse date: {date_string}")
    return date_string

def apply(data: Union[List[Dict[str, Any]], Dict[str, Any]], mapping: Dict[str, str], utility_type: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Apply a mapping to the data based on the provided mapping dictionary and utility type.

    Args:
        data (Union[List[Dict[str, Any]], Dict[str, Any]]): The input data to be transformed.
        mapping (Dict[str, str]): A dictionary defining the source to target key mapping.
        utility_type (str): A string representing the type of utility.

    Returns:
        Union[List[Dict[str, Any]], Dict[str, Any]]: The transformed data.
    """
    def map_item(item: Dict[str, Any]) -> Dict[str, Any]:
        result = {"utility_company": utility_type, "mapping" : mapping, "additional_info" : {}}
        
        for source_key, target_key in mapping.items():
            value = item
            for key in source_key.split('.'):
                value = value.get(key, {}) if isinstance(value, dict) else None
                if value is None:
                    break
            
            if value is not None:
                if target_key == "timestamp":
                    value = parse_date(str(value))
                elif target_key == "consumption_value":
                    try:
                        value = float(value)
                    except ValueError:
                        logging.warning(f"Unable to convert {value} to float for consumption_value")
                        continue
                
                if target_key in INTERNAL_SCHEMA["properties"]:
                    result[target_key] = value
                else:
                    result["additional_info"][target_key] = value
            else:
                logging.warning(f"No value found for '{source_key}' in the source data")
        
        # Set default consumption unit if not provided
        if "consumption_value" in result and "consumption_unit" not in result:
            result["consumption_unit"] = {"electricity": "kWh", "water": "cubic_meters", "gas": "m³"}.get(utility_type, "unknown")
        
        return result

    if isinstance(data, list):
        return [map_item(item) for item in data]
    elif isinstance(data, dict):
        return map_item(data)
    else:
        raise ValueError("Data must be a dictionary or a list of dictionaries")