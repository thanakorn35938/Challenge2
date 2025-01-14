import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import linregress
import json

def corrected_distances(k, m, M):
    D = 10 ** ((m - M + 5) / 5) / 1e6
    for _ in range(10):
        A_V = k * D
        m_corr = m - A_V
        D = 10 ** ((m_corr - M + 5) / 5) / 1e6
    return D

def hubble_fit(k, m, M, z, c=3.0e5):
    D_corr = corrected_distances(k, m, M)
    v_obs = c * z
    H0, intercept, _, _, _ = linregress(D_corr, v_obs)
    v_pred = H0 * D_corr
    return np.sum((v_obs - v_pred)**2)

def compute_H0(k, m, M, z, c=3.0e5):
    D_corr = corrected_distances(k, m, M)
    v_obs = c * z
    H0, intercept, _, _, _ = linregress(D_corr, v_obs)
    return H0

# Load data from JSON file
with open('Challenge2_data.json', 'r') as f:
    data = json.load(f)

apparent_magnitude = np.array(data['Apparent Magitude (m)'])
absolute_magnitude = np.array(data['Absolute Magnitude (M)'])
redshift = np.array(data['Redshift (z)'])

c = 299792.458

k_initial = 0.0

result = minimize(hubble_fit, k_initial, args=(apparent_magnitude, absolute_magnitude, redshift))

k_best = result.x[0]
hess_inv = result.hess_inv
k_error = np.sqrt(hess_inv[0][0])

D_initial = 10 ** ((apparent_magnitude - absolute_magnitude + 5) / 5) / 1e6
for _ in range(10):
    A_V = k_best * D_initial
    m_corr = apparent_magnitude - A_V
    D_initial = 10 ** ((m_corr - absolute_magnitude + 5) / 5) / 1e6

Distance_array = D_initial

Velocity_array = redshift * c

slope, intercept, r_value, p_value, std_err = linregress(Distance_array, Velocity_array)

x = np.linspace(0, 200, 10000)
y = slope * x + intercept

plt.scatter(Distance_array, Velocity_array)
plt.plot(x, y)
plt.show()

print("H0 =", slope, "±", std_err, "km/s-Mpc")
print("k =", k_best, "±", k_error, "mag/Mpc")
