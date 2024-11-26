import numpy as np
from scipy.optimize import minimize
import json
import logging
from datetime import datetime

# Set up logging
log_filename = datetime.now().strftime('logfile_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
kappa_v = 0.1  # Example value for the extinction coefficient (for a given wavelength)

# Function to calculate the total error using NumPy
def total_error(params):
    logging.info(f"Calculating total error with params: {params}")
    H0, A_V = params
    # Perform the error calculation
    if H0 <= 0 or A_V < 0:
        logging.warning(f"Unreasonable parameter values encountered: H0={H0}, A_V={A_V}")
        return np.inf
    model = m - M - 5 * np.log10(np.maximum(v / H0, 1e-10)) + 5 - H0 * kappa_v * A_V
    error = model ** 2
    total_err = np.sum(error)
    logging.info(f"Total error calculated: {total_err}")
    return total_err

# Function to read data from a JSON file
def read_data_from_json(file_path):
    logging.info(f"Reading data from JSON file: {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging.info("Data successfully read from JSON file")
    return data

# Path to the JSON file
json_file_path = 'Challenge2_data.json'

# Read data from the JSON file
data = read_data_from_json(json_file_path)

# Set the arrays with the imported data
logging.info("Setting up data arrays")
m = np.array(data['Apparent Magitude (m)'])
M = np.array(data['Absolute Magnitude (M)'])
v = np.array(data['Redshift (z)'])

# Initial guess for H0 and A_V
initial_guess = [67, 0.1]  # H0 = 67 km/s/Mpc, A_V = 0.1
logging.info(f"Initial guess for H0 and A_V: {initial_guess}")

# Minimize the total error using scipy.optimize
logging.info("Starting minimization process")
result = minimize(total_error, initial_guess, method='Powell')
logging.info("Minimization process completed")

# Output the estimated values for H0 and A_V
H0_estimated, A_V_estimated = result.x
logging.info(f"Estimated H0: {H0_estimated} km/s/Mpc")
logging.info(f"Estimated A_V: {A_V_estimated}")

print(f"Estimated H0: {H0_estimated} km/s/Mpc")
print(f"Estimated A_V: {A_V_estimated}")
