import numpy as np

# some constants
pi = np.pi # 3.14159...

# function to calculate x-distance
def anchor_calc_x(H, p, chi, theta, psi):
    return (H + chi / np.cos(psi) - p) / (np.tan(theta) + np.tan(psi))

# 1. Collect input data ##################################################

# input data
H = 8.0 # m (excavation depth)
sh = 2.0 # m (horizontal spacing)
gamma = 18.0 # kN/m³ (natural unit weight)
phi_deg = 34.0 # ° (friction angle)
theta_deg = 15.0 # ° (tendon inclinaton)

# geometric parameters
psi_deg = 45.0 + phi_deg / 2.0
psi = psi_deg * pi / 180.0
theta = theta_deg * pi / 180.0

# calculate chi
chi = np.max([1.5, H/5]) # m

# message
print(f'\n1. Collect input data')
print(f'H     = {H} m')
print(f'sh    = {sh} m')
print(f'gamma = {gamma} kN/m³')
print(f'phi   = {phi_deg}°')
print(f'theta = {theta_deg}°')
print(f'psi   = {psi_deg}°')
print(f'chi   = {chi} m')
