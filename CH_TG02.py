import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import linregress
m = np.array([14.541391237647325, 16.756128786151876, 15.829604890719585,
                               16.29457480995023, 13.829093893418786, 14.182568722430029,
                               16.03907734592769, 17.138868011663146, 15.998250803312972,
                               17.910486867901746, 15.074669722972802, 15.164039588647865,
                               12.484639187522449, 15.60165860026537, 13.753617662388354,
                               14.50453086130131, 14.147029911292748, 16.04484713334022,
                               15.192141049675008])

M = np.array([-16.339065057631082, -18.177729885179346, -16.696145000879945,
                               -19.512265201224647, -19.665756128261307, -21.24923043094372,
                               -17.778062621886992, -17.656338949942327, -19.397655426925155,
                               -16.93192787486793, -20.918615711799312, -18.86686028127157,
                               -23.32220082365243, -18.32499057478847, -21.310568461137503,
                               -18.80925829710656, -18.51036467391853, -20.29101150867485,
                               -16.313008928644898])

z = np.array([0.0036759669738346545, 0.02260424055745114, 0.008037853020448127,
                     0.036351715342596735, 0.01039452291356091, 0.03358661872848456,
                     0.014447634338827342, 0.017837996244636223, 0.030485281173716405,
                     0.025338258561158566, 0.030141298549296147, 0.017837996244636223,
                     0.0325517381815954, 0.011068888391776666, 0.01715898899234225,
                     0.01208129940826752, 0.006022296587493203, 0.03220702315577939,
                     0.004010818525698623])
D_final = []
v_final = []
for i in range(19):
    d = 10**((m[i] - M[i] - 25) / 5)  
    v = z[i] * 299792.458  
    D_final.append(d)  
    v_final.append(v)  

D_final = np.array(D_final)
v_final = np.array(v_final)

slope, intercept, r_value, p_value, std_err = linregress(D_final, v_final)

D_fit = np.linspace(min(D_final), max(D_final), 100)  # Distance range for plotting
v_fit = slope * D_fit + intercept  # Best-fit line

plt.scatter(D_final,v_final)
plt.plot(D_fit, v_fit)
plt.xlabel("Distance (Mpc)")
plt.ylabel("Recessional Velocity (km/s)")
plt.title("Hubble's Law with Best-Fit Line")
plt.show()


H0 = slope
H0_error = std_err
P_value=p_value
R_value=r_value
print(f"Hubble constant (H0): {H0:.2f} ± {H0_error:.2f} km/s/Mpc")
print(f"P Value:{P_value:.9f}")
print(f"P Value:{R_value:.9f}")