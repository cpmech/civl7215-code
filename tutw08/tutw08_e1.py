import numpy as np

# some constants
pi = np.pi # 3.14159...

# function to calculate the unbonded length
def anchor_unbonded_length(d, H, chi, theta, psi, strand = False):

    # minimum overburden depth
    z_min = 4.5 # m

    # minimum unbonded length
    Lub_min = 4.5 if strand else 3.0 # m

    # trial horizontal distance of bonded-length-tip
    x_trial = (H - d + chi / np.cos(psi)) / (np.tan(theta) + np.tan(psi))

    # minimum horizontal distance of bonded-length-tip
    if d < z_min:
        x_min = (z_min - d) / np.tan(theta)
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

# 1. Collect input data #######################################################

# input data
H = 9.0 # m (excavation depth)
Sh = 2.0 # m (horizontal spacing)
gamma = 18.0 # kN/m³ (natural unit weight)
phi_deg = 34.0 # ° (friction angle)
theta_deg = 15.0 # ° (tendon inclinaton)

# slope of potential slip line
psi_deg = 45.0 + phi_deg / 2.0

# angles in radians
phi = phi_deg * pi / 180.0
theta = theta_deg * pi / 180.0
psi = psi_deg * pi / 180.0

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

# 2. Calculate unbonded length of anchor # 1 ###################################

# depth of head of anchor # 1
H1 = 3.0
d1 = 3.0

# unbonded length of anchor # 1
print(f'\n2. Calculate unbonded length of anchor # 1')
Lub1 = anchor_unbonded_length(d1, H, chi, theta, psi)

# 3. Calculate unbonded length of anchor # 2 ###################################

# depth of head of anchor # 2
H2 = 3.0
d2 = d1 + H2

# unbonded length of anchor # 2
print(f'\n3. Calculate unbonded length of anchor # 2')
Lub2 = anchor_unbonded_length(d2, H, chi, theta, psi)

# 4. Calculate the maximum lateral earth pressure ##############################

# coefficient of the active lateral earth pressure
Ka = (1.0 - np.sin(phi)) / (1.0 + np.sin(phi))

# total lateral thrust
Pa = 0.65 * Ka * gamma * H**2.0

# maximum lateral earth pressure
H3 = 3.0
p = Pa / (H - H1/3.0 - H3/3.0)

# message
print(f'\n4. Calculate the maximum lateral earth pressure')
print(f'Ka = {Ka:.3f}')
print(f'Pa = {Pa:.1f} kN/m')
print(f'p  = {p:.1f} kPa')

# 5. Calculate the horizontal anchor loads #####################################

# horizontal anchor load # 1
Th1 = (2.0*H1/3.0 + H2/2.0) * p

# horizontal anchor load # 2
Th2 = (H2/2.0 + 23.0*H3/48.0) * p

# message
print(f'\n5. Calculate the horizontal anchor loads')
print(f'Th1 = {Th1:.1f} kN/m')
print(f'Th2 = {Th2:.1f} kN/m')

# 6. Calculate the anchor design loads #########################################

# anchor design load # 1
A1 = Th1 * Sh / np.cos(theta)

# anchor design load # 2
A2 = Th2 * Sh / np.cos(theta)

# message
print(f'\n6. Calculate anchor design loads')
print(f'A1 = {A1:.1f} kN')
print(f'A2 = {A2:.1f} kN')

# 7. Determine the steel bar diameter and trumpet opening size ################

# max anchor load
Ai_max = np.max([A1, A2])

# selecting 26 mm bar, thus from the first line in Table 9.4
smts_60 = 0.6 * 568.0

# check 60% SMTS
status = 'OK' if Ai_max <= smts_60 else 'not OK'

# for the 26 mm bar, from Table 9.6 the trumpet opening size is
d_DH = 64.0 / 1000.0

# message
print(f'\n7. Determine the steel bar diameter and trumpet opening size')
print(f'Ai_max    = {Ai_max:.1f} kN')
print(f'60 % SMTS = {smts_60} kN ({status})')
print(f'd_DH      = {d_DH*1000} mm')

# 8. Calculate the bonded and total lengths ####################################

# from Table 9.2, for a Medium dense sand with SPT 20, assume
tau_a = 400.0 # kPa

# bonded and total length of anchor # 1
Lb1 = A1 / (pi * d_DH * tau_a)
L1 = Lub1 + Lb1

# bonded and total length of anchor # 1
Lb2 = A2 / (pi * d_DH * tau_a)
L2 = Lub2 + Lb2

# message
print(f'\n8. Calculate the bonded and total lengths')
print(f'Lb1 = {Lb1:.1f} m')
print(f'Lb2 = {Lb2:.1f} m')
print(f'L1  = {L1:.1f} m')
print(f'L2  = {L2:.1f} m')
