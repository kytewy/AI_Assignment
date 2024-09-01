import os
from dotenv import load_dotenv
from data.schema import INTERNAL_SCHEMA

def load_config():
    load_dotenv()

    return {
            "internal_schema": INTERNAL_SCHEMA,
            "data_sources": {
                "easy_electricity": {
                "credentials": {
                    "username": "elec_user",
                    "password": "elec_pass"
                }
                },
                "nested_heat": {
                "credentials": {
                    "username": "nested_elec_user",
                    "password": "nested_elec_pass"
                }
                },
                "wrong_credentials_water": {
                "credentials": {
                    "username": "water_user",
                    "password": "wrong_pass"
                }
                }
            },
            "output_directory": "output"
        }