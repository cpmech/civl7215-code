import numpy as np

# 1. Collect data regarding the soil ##########################################

# cohesion, friction angle, and unit weight
c = 2.0 # kPa
phi = 32.0 * np.pi / 180.0 # °
gamma = 18.5 # kN/m³

# message
print(f'\n1. Collect data regarding the soil')
print(f'c     = {c} kPa')
print(f'phi   = {phi * 180.0 / np.pi:.1f} °')
print(f'gamma = {gamma} kN/m³')

# 2. Collect data regarding the excavation ####################################

# factors of safety
FS_glob = 1.5 # global
FS_po = 2.0 # pullout

# batter, backslope, and depth of excavation
omega = 10.0 # ° (batter angle)
beta = 0.0 # ° (backslope angle)
H = 9.0 # m (height)

# message
print(f'\n2. Collect data regarding the excavation')
print(f'FS_glob          = {FS_glob}')
print(f'FS_po            = {FS_po}')
print(f'omega (batter)   = {omega}')
print(f'beta (backslope) = {beta}')
print(f'H (height)       = {H}')

# 3. Decide on spacing, drill hole diameter, and bond strength #################

# horizontal and vertical spacing
s_h = 1.5 # m
s_v = 1.5 # m
s_max = np.max([s_h, s_v])

# diameter of drill holes
d_DH = 150.0 / 1000.0 # m

# ultimate bond strength between nail and soil
tau_u = 125.0 # kPa

# message
print(f'\n3. Decide on spacing, drill hole diameter, and bond strength')
print(f's_h   = {s_h} m')
print(f's_v   = {s_v} m')
print(f's_max = {s_max} m')
print(f'd_DH  = {d_DH*1000} mm')
print(f'tau_u = {tau_u} kPa')

# 4. Read the reference nail length and design force from charts ###############

# normalized pullout resistance
mu_po = tau_u * d_DH / (FS_po * gamma * s_h * s_v)

# normalized cohesion
c_star = c / (gamma * H)

# read (L/H) and tmaxs from Figure 9.30
LbyH_chart = 0.6
tmaxs_chart = 0.16

# message
print(f'\n4. Read the reference nail length and design force from charts')
print(f'mu_po       = {mu_po:.3f}')
print(f'c_star      = {c_star:.4f}')
print(f'LbyH_chart  = {LbyH_chart}')
print(f'tmaxs_chart = {tmaxs_chart}')

# 5. Apply correction factors ##################################################

# read correction factors from Figure 9.32
C1L = 0.82
C1F = 1.47

# calculate other correction factors
C2L = np.max([0.85, -4.0*c_star + 1.09])
C3L = np.max([1.0, 0.52*FS_glob + 0.3])
C2F = C2L

# calculate (L/H) and (tmaxs) corrected
LbyH = C1L * C2L * C3L * LbyH_chart
tmaxs = C1F * C2F * tmaxs_chart

# message
print(f'\n5. Apply correction factors')
print(f'C1L   = {C1L}')
print(f'C2L   = {C2L:.2f}')
print(f'C3L   = {C3L:.2f}')
print(f'LbyH  = {LbyH:.2f}')
print(f'tmaxs = {tmaxs:.2f}')

# 6. Calculate the length of nails ############################################

# length of soil nails
L_calc = LbyH * H

# select length of soil nails
L = 5.0 # m

# message
print(f'\n6. Calculate the length of nails')
print(f'L (calc)     = {L_calc:.2} m')
print(f'L (selected) = {L:.2} m')

# 7. Calculate the nail forces ################################################

# maximum design nail force
Tmaxs = tmaxs * gamma * H * s_h * s_v

# design nail force at the nail head
T0 = Tmaxs * (0.6 + 0.2 * (s_max - 1.0))

# message
print(f'\n7. Calculate the nail forces')
print(f'Tmaxs = {Tmaxs:.1f} kN')
print(f'T0    = {T0:.1f} kN')

# 8. Select the nail bar diameter #############################################

# select grade 420 steel
fy = 420 * 1000 # kPa
FS_T = 1.8

# calculate cross-sectional area of the nail bar
A_nb = Tmaxs * FS_T / fy

# select a threaded bar diameter
d_bar = 25.0 # mm
A_bar = 510.0 # mm

# check cross-sectional area of bar
check_area = 'OK' if A_bar >= A_nb else 'fail'

# check grout cover
min_cover = 25.0 # mm
d_total = d_bar + 2.0 * min_cover # mm
check_cover = 'OK' if d_total < d_DH*1000.0 else 'fail'

# message
print(f'\n8. Select the nail bar diameter')
print(f'fy          = {fy} kPa')
print(f'FS_T        = {FS_T}')
print(f'A_nb        = {A_nb*1e6:.1f} mm²')
print(f'd_bar       = {d_bar} mm')
print(f'A_bar       = {A_bar:.1f} mm²')
print(f'check_area  = {check_area}')
print(f'd_total     = {d_total} mm')
print(f'check_cover = {check_cover}')
