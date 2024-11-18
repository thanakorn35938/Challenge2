import cupy as cp
from scipy.optimize import minimize

# Example dataset arrays (replace with your real data)
m = cp.array([...])  # Apparent magnitudes as a GPU array
M = cp.array([...])  # Absolute magnitudes as a GPU array
v = cp.array([...])  # Velocities as a GPU array

# Constants
kappa_v = 0.1  # Example value for the extinction coefficient (for a given wavelength)

# Function to calculate the total error using GPU (CuPy)
def total_error(params):
    H0, A_V = params
    # Initialize error as zero
    error = cp.zeros_like(m)
    
    # Perform the error calculation in parallel (on GPU)
    for i in range(len(m)):
        model = m[i] - M[i] - 5 * cp.log10(v[i] / H0) + 5 - H0 * kappa_v * A_V
        error[i] = model ** 2
    
    # Return the total error (sum of all individual errors)
    return cp.sum(error).get()  # .get() moves the result from GPU to CPU

# Initial guess for H0 and A_V
initial_guess = [70, 0.1]  # H0 = 70 km/s/Mpc, A_V = 0.1

# Minimize the total error using scipy.optimize with CuPy support
result = minimize(total_error, initial_guess, method='Nelder-Mead')

# Output the estimated values for H0 and A_V
H0_estimated, A_V_estimated = result.x
print(f"Estimated H0: {H0_estimated} km/s/Mpc")
print(f"Estimated A_V: {A_V_estimated}")
