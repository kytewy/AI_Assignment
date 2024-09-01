import json
import logging
from llm.client import OpenAIClient

def get_mapping_from_llm(client: OpenAIClient, internal_schema, external_data_sample):
    prompt = f"""
    Task: Create a Python dictionary that maps external data fields to internal schema fields for utility consumption data.

    Internal Schema:
    {json.dumps(internal_schema, indent=2)}

    External Data Sample:
    {json.dumps(external_data_sample, indent=2)}

    Requirements:
    1. Create a Python dictionary where keys are external field names and values are corresponding internal field names.
    2. Only include fields that have a clear correspondence between external and internal schemas.
    3. Handle nested structures and unit conversions if necessary.
    4. Return only the Python dictionary, no explanations.

    Example Output Format:
    {{
        "external_field1": "internal.nested.field1",
        "external_field2": "internal_field2"
    }}

    DO NOT leave in ```python ``` before the dictionary.
    """

    messages = [
        {"role": "system", "content": "You are a data engineer specializing in utility consumption data, creating field mappings between complex schemas."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.generate_chat_completion(messages)
        if response:
            return json.loads(response)
        else:
            raise ValueError("Empty response from LLM")
    except json.JSONDecodeError:
        logging.error(f"Failed to parse LLM response as JSON: {response}")
        raise
    except Exception as e:
        logging.error(f"Error in getting mapping from LLM: {str(e)}")
        raise

