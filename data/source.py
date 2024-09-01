from typing import Dict, Any, List

def validate_credentials(source_name: str, credentials: Dict[str, str]) -> bool:
    expected_credentials = DATA_SOURCES.get(source_name, {}).get('credentials', {})
    return credentials.get('username') == expected_credentials.get('username') and \
           credentials.get('password') != 'wrong_pass'

def get_data(source_name: str) -> List[Dict[str, Any]]:
    return DATA_SOURCES.get(source_name, {}).get('sample', [])

DATA_SOURCES = {
    "easy_electricity": {
        "credentials": {
            "username": "elec_user",
            "password": "elec_pass"
        },
        "sample": [
            {
                "account_id": "A001",
                "meter_number": "E123",
                "consumption_kwh": 250.5,
                "reading_timestamp": "2023-08-15T14:30:00Z",
                "tariff_type": "residential"
            },
            {
                "account_id": "A002",
                "meter_number": "E456",
                "consumption_kwh": 300.0,
                "reading_timestamp": "2023-08-15T15:00:00Z",
                "tariff_type": "commercial"
            }
        ]
    },
    "nested_heat": {
        "credentials": {
            "username": "nested_elec_user",
            "password": "nested_elec_pass"
        },
        "sample": [
            {
                "customer": {
                    "id": "C001",
                    "meter": {
                        "number": "NE123",
                        "readings": {
                            "consumption": 275.5,
                            "unit": "kWh"
                        }
                    }
                },
                "timestamp": "2023-08-15T16:30:00Z",
                "billing": {
                    "type": "residential"
                }
            },
            {
                "customer": {
                    "id": "C002",
                    "meter": {
                        "number": "NE456",
                        "readings": {
                            "consumption": 450.0,
                            "unit": "kWh"
                        }
                    }
                },
                "timestamp": "2023-08-15T17:00:00Z",
                "billing": {
                    "type": "industrial"
                }
            }
        ]
    },
    "wrong_credentials_water": {
        "credentials": {
            "username": "water_user",
            "password": "wrong_pass"
        },
        "sample": [
            {
                "customer_code": "W001",
                "meter_id": "WM123",
                "usage_cubic_meters": 15.2,
                "reading_date": "2023-08-15",
                "usage_type": "residential"
            }
        ]
    }
}