import json
import logging

# Set up logging configuration
logging.basicConfig(filename='clc_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # Assuming the keys are present in the data for Apparent Magnitude (m), Absolute Magnitude (M), and Redshift (z)
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
        return None  # Ensure None is returned in case of error
    
    # Transform data
    transformed_data = transform_data(data)
    if transformed_data is None:
        logging.error("Exiting due to data transformation error.")
        return None
    
    # Display the transformed data
    for i, row in enumerate(transformed_data, 1):
        print(f"{i} = {row}")
        logging.info(f"Row {i} = {row}")
    
    return transformed_data  # Ensure the transformed data is returned

# Function to multiply the n-th column by a variable (like the speed of light)
def multiply_column(data, column_index, x):
    """
    Multiplies the specified column (by column_index) in the data by the variable x.
    
    Parameters:
    - data: The 2D list (matrix).
    - column_index: The column to multiply (0-based index).
    - x: The multiplier (could be the speed of light or any other value).
    
    Returns:
    - The modified data with the specified column multiplied by x.
    """
    # Check if 'data' is None
    if data is None:
        logging.error("Input 'data' is None")
        return None

    try:
        # Ensure column_index is within bounds
        if column_index < 0 or column_index >= len(data[0]):
            raise IndexError("Column index is out of bounds")

        # Multiply the specified column by the variable x
        for row in data:
            row[column_index] *= x
        
        # Print and log the modified data
        for i, row in enumerate(data, 1):
            logging.info(f"Row {i} after multiplying column {column_index + 1}: {row}")
            print(f"Row {i} after multiplying column {column_index + 1}: {row}")
        
        return data
    
    except Exception as e:
        logging.error(f"Error in column multiplication: {e}")
        return None

# Run the main function with the path to your JSON file
file_path = 'Challenge2_data.json'  # Replace with the path to your JSON file
trans_data = main(file_path)  # This will now return the transformed data

# If transformation was successful, perform column multiplication on a specific column
if trans_data is not None:
    column_index = 2  # For example, multiplying the third column (index 2) - Redshift column
    x = 299792458  # Speed of light in meters per second (example multiplier)
    
    # Call multiply_column to multiply the specific column by the multiplier x
    modified_data = multiply_column(trans_data, column_index, x)
