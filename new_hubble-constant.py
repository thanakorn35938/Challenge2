import json
import logging
import numpy as np
from datetime import datetime

# Set up logging configuration
log_filename = datetime.now().strftime('logfile_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
###  End of Basics Setup ###

### Start of Functions Declaration ###
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
    ### End of Function ###

def transform_data(data):
    logging.info("Starting data transformation.")
    try:
        transformed_data = np.array([data["Apparent Magitude (m)"], data["Absolute Magnitude (M)"], data["Redshift (z)"]]).T
        logging.info("Data transformation completed successfully.")
        return transformed_data
    except Exception as e:
        logging.error(f"Error in data transformation: {e}")
        return None
    ### End of Function ###
    

def calculate_expression(data, column_index, c):
    if data is None:
        logging.error("Input 'data' is None")
        return None

    try:
        if column_index < 0 or column_index >= data.shape[1]:
            raise IndexError("Column index is out of bounds")

        col = data[:, column_index]
        result = (((col + 1)**2 - 1) / ((col + 1)**2 + 1)) * c

        formatted_result = np.array2string(result, formatter={'float_kind':lambda x: "%.10f" % x})
        logging.info(f"Calculated result for column {column_index + 1}: {formatted_result}")
        print(f"Calculated result for column {column_index + 1}: {formatted_result}")

        return result
    except Exception as e:
        logging.error(f"Error in calculating expression: {e}")
        return None
    ### End of Function ###

def velocity_calc(data, col1, col2):
    if data is None:
        logging.error("Input 'data' is None")
        return None

    try:
        if col1 < 0 or col1 >= data.shape[1] or col2 < 0 or col2 >= data.shape[1]:
            raise IndexError("Column index is out of bounds")

        column1 = data[:, col1]
        column2 = data[:, col2]
        result = (10**((column1 - column2 + 5) / 5)) / 10**6

        formatted_result = np.array2string(result, formatter={'float_kind':lambda x: "%.10f" % x})
        logging.info(f"Calculated velocity for columns {col1 + 1}, {col2 + 1}: {formatted_result}")
        print(f"Calculated velocity for columns {col1 + 1}, {col2 + 1}: {formatted_result}")

        return result
    except Exception as e:
        logging.error(f"Error in calculating velocity: {e}")
        return None
    ### End of Function ###

def file_loader(file_path):
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
### End of Function ###
### End of Functions Declaration ###

if __name__ == "__main__":
    file_path = 'Challenge2_data.json'
    trans_data = file_loader(file_path)

    if trans_data is not None:
        column_index = 2
        c = 299792458
        calculated_result = calculate_expression(trans_data, column_index, c)
        print(calculated_result)
        velocity_data = velocity_calc(trans_data, 0, 1)
        print(velocity_data)