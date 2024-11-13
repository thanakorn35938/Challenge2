import json
import logging

# Set up logging configuration
logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load data from a JSON file
def load_data_from_json(file_path):
    logging.info(f"Attempting to load data from {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logging.info("Data loaded successfully from JSON file.")
        return data
    except Exception as e:
        logging.error(f"Failed to load data from JSON file: {e}")
        return None

# Function to transform data to the desired format
def transform_data(data):
    logging.info("Starting data transformation.")
    try:
        transformed_data = [[m, M, z] for m, M, z in zip(data["Apparent Magitude (m)"], data["Absolute Magnitude (M)"], data["Redshift (z)"])]
        logging.info("Data transformation completed successfully.")
        return transformed_data
    except Exception as e:
        logging.error(f"Error in data transformation: {e}")
        return None

# Main function to execute the process
def main(file_path):
    # Load data
    data = load_data_from_json(file_path)
    if data is None:
        logging.error("Exiting due to data loading error.")
        return
    
    # Transform data
    transformed_data = transform_data(data)
    if transformed_data is None:
        logging.error("Exiting due to data transformation error.")
        return
    
    # Display the transformed data
    for i, row in enumerate(transformed_data, 1):
        print(f"{i} = {row}")
        logging.info(f"Row {i} = {row}")

# Run the main function with the path to your JSON file
file_path = 'Challenge2_data.json'  # replace with the path to your JSON file
main(file_path)
