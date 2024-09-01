# Data Processing Project

This project is designed to process data from various sources, transform it using AI-generated mappings, and validate the results. It uses OpenAI's API for generating mappings and includes features for credential validation, data transformation, and error handling.

## Project Structure

- `config.py`: Loads configuration settings
- `data/`:
  - `source.py`: Contains functions for data retrieval and credential validation
  - `map.py`: Includes the `apply` function for data transformation
  - `validator.py`: Contains the `validate_data` function
- `llm/`:
  - `mapper.py`: Includes the `get_mapping_from_llm` function
  - `client.py`: Contains the `OpenAIClient` class
- `utils/`:
  - `logging.py`: Sets up logging for the project

## Overview

This script orchestrates the entire data processing pipeline:

1. Loads configuration
2. Sets up logging
3. Processes each data source:
   - Validates credentials
   - Retrieves sample data
   - Generates mapping using OpenAI
   - Transforms data
   - Validates transformed data
   - Saves valid and invalid data

## Setup

1. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set up your configuration file (see Configuration section)
3. Ensure you have an OpenAI API key

## Configuration

Create a configuration file (e.g., `config.json`) with the following structure:

```json
{
	"output_directory": "path/to/output",
	"data_sources": {
		"source1": {
			"credentials": {
				"username": "user1",
				"password": "pass1"
			}
		},
		"source2": {
			"credentials": {
				"username": "user2",
				"password": "pass2"
			}
		}
	},
	"internal_schema": {
		// Your internal schema definition
	}
}
```

## Usage

Run the main script:

```
python main.py
```

This will process all configured data sources and save the results in the specified output directory.

## Output

The script generates two types of output files for each data source:

- `{source_name}_valid_data.json`: Contains the successfully transformed and validated data
- `{source_name}_invalid_data.json`: Contains data that failed validation

### Expected Output

When running the script, you should see output similar to the following:

```
****************************************
Starting to process for source1
Loading raw data for source1
Generated Mapping for source1
Transforming data from source1
Successfully validated 2 items from source1
Data saved to path/to/output/source1_valid_data.json

****************************************
Starting to process for source2
Loading raw data for source2
Generated Mapping for source2
Transforming data from source2
Successfully validated 1 items from source2
1 validation errors occurred for source2.
Data saved to path/to/output/source2_valid_data.json
Data saved to path/to/output/source2_invalid_data.json
```

## Logging

The script logs its progress and any errors to the console and potentially to a log file, depending on the logging configuration in `utils/logging.py`.

## Error Handling

- Invalid credentials will stop the processing for that particular data source
- Validation errors are logged, and the invalid data is saved separately

## Extending the Project

To add a new data source:

1. Add its configuration to the config file
2. Implement any necessary data retrieval logic in `data/source.py`
3. If needed, update the transformation logic in `data/map.py`

To modify the validation rules, update the `validate_data` function in `data/validator.py`.

## Dependencies

This project's dependencies are listed in the `requirements.txt` file. You can install all required packages using pip:

```
pip install -r requirements.txt
```

Make sure to keep this file updated if you add or remove any dependencies from the project.

# Areas of Improvement

### AI Agent with Validation Feedback

Currently, we call the LLM once to generate the mapping. By incorporating feedback from the validation process, we could adapt and improve the data processing pipeline over time. Here's how:

1. Learning from Errors

   - Analyze invalid data and reasons for validation failures
   - Identify error patterns to improve future mapping strategies

2. Adaptive Mapping

   - Dynamically adjust mapping rules based on validation results
   - Implement robust strategies for recurring error types

3. Proactive Data Cleaning

   - Identify and clean common data issues pre-validation

4. Feedback Loop

   - Use each processing cycle to improve performance continuously

5. Anomaly Detection
   - Flag unusual patterns in validated data that might indicate underlying issues

This approach transforms the system from a static pipeline to a dynamic, self-improving process, enhancing accuracy and efficiency over time.

### Asynchronous Processing

Our current synchronous approach may become a bottleneck when scaling to multiple LLM calls and database connections. Asynchronous processing offers a solution:

- Multiple API calls
- Database queries
- File I/O operations

#### Key Benefits

1. Improved Performance
   - Multiple operations progress simultaneously
2. Better Resource Utilization
   - CPU handles other tasks during I/O wait times
3. Enhanced Responsiveness
   - Prevents UI freezing in user-facing applications

Asynchronous processing allows the program to continue execution while waiting for I/O-bound operations, significantly improving efficiency and scalability.
