import numpy as np

# some constants
pi = np.pi # 3.14159...

# function to calculate the unbonded length
def anchor_unbonded_length(h, H, chi, theta, psi, strand = False):

    # minimum overburden depth
    z_min = 4.5 # m

    # minimum unbonded length
    Lub_min = 4.5 if strand else 3.0 # m

    # trial horizontal distance of bonded-length-tip
    x_trial = (H - h + chi / np.cos(psi)) / (np.tan(theta) + np.tan(psi))

    # minimum horizontal distance of bonded-length-tip
    if h < z_min:
        x_min = (z_min - h) / np.tan(theta)
    else:
        x_min = x_trial

    # final horizontal distance of bonded-length-tip
    x = np.max([x_trial, x_min])

    # trial unbonded length
    Lub_trial = x / np.cos(theta)

    # final unbonded length
    Lub = np.max([Lub_trial, Lub_min])

    # message
    print(f'x (trial)   = {x_trial:.1f} m')
    print(f'x (min)     = {x_min:.1f} m')
    print(f'x (final)   = {x:.1f} m')
    print(f'Lub (trial) = {Lub_trial:.1f} m')
    print(f'Lub (min)   = {Lub_min:.1f} m')
    print(f'Lub (final) = {Lub:.1f} m')

    # results
    return Lub

# 1. Collect input data ##################################################

# input data
H = 9.0 # m (excavation depth)
Sh = 2.0 # m (horizontal spacing)
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
print(f'Sh    = {Sh} m')
print(f'gamma = {gamma} kN/m³')
print(f'phi   = {phi_deg}°')
print(f'theta = {theta_deg}°')
print(f'psi   = {psi_deg}°')
print(f'chi   = {chi} m')

# 2. Calculate unbonded length of anchor # 1 #############################

# depth of head of anchor # 1
h1 = 3.0

# unbonded length of anchor # 1
print(f'\n2. Calculate unbonded length of anchor # 1')
Lub1 = anchor_unbonded_length(h1, H, chi, theta, psi)

# 3. Calculate unbonded length of anchor # 2 #############################

# depth of head of anchor # 2
h2 = 6.0

# unbonded length of anchor # 2
print(f'\n3. Calculate unbonded length of anchor # 2')
Lub2 = anchor_unbonded_length(h2, H, chi, theta, psi)

