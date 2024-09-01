import logging
import json
import os
from config import load_config
from data.source import get_data, validate_credentials
from data.map import apply
from data.validator import validate_data
from llm.mapper import get_mapping_from_llm
from llm.client import OpenAIClient
from utils.logging import setup_logging


def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logging.info(f"Data saved to {filename}")

def process_data(config):
    setup_logging()
    client = OpenAIClient(api_key=os.getenv('OPENAI_API_KEY'))
    output_dir = config['output_directory']
    os.makedirs(output_dir, exist_ok=True)

    for source_name, source_info in config['data_sources'].items():
        logging.info(f"*" * 40)
        logging.info(f"Starting to process for {source_name}")

        if not validate_credentials(source_name, source_info['credentials']):
            logging.error(f"Invalid credentials for {source_name}. Stopping processing.")
            break 
    
        # Get sample data with credentials
        sample_data = get_data(source_name)
        logging.info(f"Loading raw data for {source_name}")

        # Get mapping from LLM
        mapping = get_mapping_from_llm(client, config['internal_schema'], sample_data)            
        logging.info(f"Generated Mapping for {source_name}")

        # Transform data
        transformed_data = apply(sample_data, mapping, source_name)
        logging.info(f"Transforming data from {source_name}")

        # Validate transformed data
        errors, valid_data = validate_data(transformed_data, source_name)

        if valid_data:
            save_data(transformed_data, f"{output_dir}/{source_name}_valid_data.json")
        
        if errors:
            save_data(transformed_data, f"{output_dir}/{source_name}_invalid_data.json")
            logging.warning(f"{len(errors)} validation errors occurred for {source_name}.")


if __name__ == "__main__":
    config = load_config()
    process_data(config)