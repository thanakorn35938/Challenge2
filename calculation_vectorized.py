import json
import logging
import numpy as np

# Set up logging configuration
logging.basicConfig(filename='2.23-15-11-24.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def transform_data(data):
    logging.info("Starting data transformation.")
    try:
        transformed_data = np.array([data["Apparent Magitude (m)"], data["Absolute Magnitude (M)"], data["Redshift (z)"]]).T
        logging.info("Data transformation completed successfully.")
        return transformed_data
    except Exception as e:
        logging.error(f"Error in data transformation: {e}")
        return None

def multiply_column(data, column_index, x):
    if data is None:
        logging.error("Input 'data' is None")
        return None

    try:
        if column_index < 0 or column_index >= data.shape[1]:
            raise IndexError("Column index is out of bounds")

        data[:, column_index] *= x

        formatted_data = np.array2string(data, formatter={'float_kind':lambda x: "%.10f" % x})
        logging.info(f"Data after multiplying column {column_index + 1}: {formatted_data}")
        print(f"Data after multiplying column {column_index + 1}: {formatted_data}")

        return data
    except Exception as e:
        logging.error(f"Error in column multiplication: {e}")
        return None

def main(file_path):
    data = load_data_from_json(file_path)
    if data is None:
        logging.error("Exiting due to data loading error.")
        return None

    transformed_data = transform_data(data)
    if transformed_data is None:
        logging.error("Exiting due to data transformation error.")
        return None

    formatted_data = np.array2string(transformed_data, formatter={'float_kind':lambda x: "%.10f" % x})
    logging.info(f"Transformed data: {formatted_data}")
    print(f"Transformed data: {formatted_data}")

    return transformed_data

if __name__ == "__main__":
    file_path = 'Challenge2_data.json'
    trans_data = main(file_path)

    if trans_data is not None:
        column_index = 2
        x = 299792458
        modified_data = multiply_column(trans_data, column_index, x)