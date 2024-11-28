import numpy as np
from scipy.optimize import minimize
import json
import logging
from datetime import datetime

# Configure logging
log_filename = datetime.now().strftime('logfile_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read data from JSON file
def json_reader(file_path):
    logging.info(f"Reading data from {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging.info("Data successfully read from JSON file")
    return data

data = json_reader('Challenge2_data.json')
apparent_magnitudes = np.array(data['Apparent Magitude (m)'])
absolute_magnitudes = np.array(data['Absolute Magnitude (M)'])
z = np.array(data['Redshift (z)'])

# Calculate radial velocities from redshift (v = c * z)
c_kms = 299792.458  # Speed of light in km/s
radial_velocities = c_kms * z
bounds=[(50, 100), (0,1)]

logging.info("Radial velocities calculated from redshift")

# Define the model function with distance-dependent extinction
def magnitude_model(params, v, M):
    H0, gamma = params  # gamma is the extinction coefficient
    d = v / H0  # Distance in Mpc
    A_V = gamma * d  # Distance-dependent extinction
    m_model = M + 5 * np.log10(d) + 25 + A_V  # 25 is added for distance in Mpc
    return m_model

# Define the residuals function
def residuals(params, v, M, m_obs):
    m_model = magnitude_model(params, v, M)
    return m_obs - m_model

# Initial guesses for parameters: H0 (Hubble constant), gamma (extinction coefficient)
initial_guess = [70, 0.5]
logging.info(f"Initial guess for parameters: H0={initial_guess[0]}, gamma={initial_guess[1]}")

# Minimize the sum of squared residuals
logging.info("Starting optimization process")
result = minimize(
    lambda params: np.sum(residuals(params, radial_velocities, absolute_magnitudes, apparent_magnitudes)**2),
    initial_guess,
    bounds=bounds  # Updated bounds applied here
)

# Extract best-fit parameters
H0_best, gamma_best = result.x
logging.info(f"Optimization completed. Best-fit parameters: H0={H0_best:.2f}, gamma={gamma_best:.4f}")

# Print results
print(f"Best-fit Hubble constant (H0): {H0_best:.2f} km/s/Mpc")
print(f"Best-fit extinction coefficient (gamma): {gamma_best:.4f} mag/Mpc")

# Save the results to a JSON file
output_data = {
    'Hubble constant (H0)': H0_best,
    'Extinction coefficient (gamma)': gamma_best
}

output_file_path = 'optimization_results.json'
logging.info(f"Saving results to {output_file_path}")
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)
logging.info("Results successfully saved to JSON file")
