import numpy as np
from scipy.optimize import minimize
import json
import logging
from datetime import datetime


#Constant Define
c = 299792458
c_kms = 299792.458
# Configure logging
log_filename = datetime.now().strftime('logfile_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# JSON Reader module
def json_reader(file_path):
    logging.info(f"Reading data from JSON file: {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging.info("Data successfully read from JSON file")
    return data

logging.info("Setting up data arrays")
file_path = 'Challenge2_data.json'
data = json_reader(file_path)
apparent_magnitudes = np.array(data['Apparent Magitude (m)'])
absolute_magnitudes = np.array(data['Absolute Magnitude (M)'])
z = np.array(data['Redshift (z)'])
radial_velocities = []

logging.info("Calculating radial velocities")
for x in z:
    radial_velocities.append((((1 + x)**2 - 1) / ((1 + x)**2 + 1))*c_kms)
radial_velocities = np.array(radial_velocities)

logging.info("Defining the model function")
# Define the model function
def magnitude_model(params, v, M):
    H0, R_V, E_BV = params
    A_V = R_V * E_BV
    m_model = M + 5 * np.log10(v / H0) - 5 + A_V
    return m_model

logging.info("Defining the residuals function")
# Define the residuals function
def residuals(params, v, M, m_obs):
    m_model = magnitude_model(params, v, M)
    return m_obs - m_model

# Initial guesses for parameters: H0 (Hubble constant), R_V (extinction ratio), E(B-V) (color excess)
initial_guess = [70, 3.1, 0.1]

logging.info("Starting optimization process")
# Minimize the sum of squared residuals
result = minimize(
    lambda params: np.sum(residuals(params, radial_velocities, absolute_magnitudes, apparent_magnitudes)**2),
    initial_guess,
    bounds=[(50, 100), (2.0, 5.0), (0.0, 1.0)]  # Reasonable bounds for H0, R_V, E(B-V)
)

logging.info("Optimization process completed")
# Extract best-fit parameters
H0_best, R_V_best, E_BV_best = result.x

# Print results
logging.info(f"Best-fit Hubble constant (H0): {H0_best:.2f} km/s/Mpc")
logging.info(f"Best-fit R_V: {R_V_best:.2f}")
logging.info(f"Best-fit E(B-V): {E_BV_best:.2f}")

print(f"Best-fit Hubble constant (H0): {H0_best:.2f} km/s/Mpc")
print(f"Best-fit R_V: {R_V_best:.2f}")
print(f"Best-fit E(B-V): {E_BV_best:.2f}")
# Save the results to a JSON file
output_data = {
    'Hubble constant (H0)': H0_best,
    'R_V': R_V_best,
    'E(B-V)': E_BV_best
}

output_file_path = datetime.now().strftime('output_js_%Y%m%d_%H%M%S.json')
logging.info(f"Saving optimization results to JSON file: {output_file_path}")
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)
logging.info("Optimization results successfully saved to JSON file")