import numpy as np

'''
* 20 m thick soft clay
* undrained strength of 20 kPa
* groundwater table 1 m deep
* unit weights: dry = 18 kN/m3, wet = 19 kN/m³
* square footing: width = 2 m
* embedment depth of 1 m
* applied load + footing weight = 400 kN
* FS required of 2.5
* granular columns 10 m long, triangular pattern, spacing of 1.5 m, dc = 0.8m
'''

# some constants
gw = 9.81 # kN/m³ unit weight of water
pi = np.pi # 3.14159...
sr2 = np.sqrt(2.0)
sr3 = np.sqrt(3.0)

# function to compute the area replacement ratio
def calc_area_repl_ratio(dc, s, triangular_pattern = False):
    C = pi / (2.0 * sr3) if triangular_pattern else  pi / 4.0
    return C * (dc / s) ** 2.0

# 1. Collect soft clay data ##############################################

# undrained strength and unit weights
soil_cu = 20.0 # kPa
soil_gamma_dry = 18.0 # kN/m³
soil_gamma_wet = 19.0 # kN/m³

# message
print(f'\n1. Collect soft clay data')
print(f'soil        cu = {soil_cu} kPa')
print(f'soil gamma dry = {soil_gamma_dry} kN/m³')
print(f'soil gamma wet = {soil_gamma_wet} kN/m³')

# 2. Collect footing data and compute stress #############################

# footing data
foot_depth = 1.0 # m
foot_width = 2.0 # m
foot_area = foot_width * foot_width # m²

# compute applied bearing pressure at the base of the footing
load = 400.0 # kN
pressure = load / foot_area

# compute effective overburden stress at the base of the footing
sig_overb_eff = foot_depth * soil_gamma_dry # kPa

# message
print(f'\n2. Collect footing data and compute stress')
print(f'area of the footing         = {foot_area} m²')
print(f'pressure at base of footing = {pressure} kN/m²')
print(f'effective overburden stress = {sig_overb_eff} kPa')

# 3. Collect granular columns data #######################################

# diameter and spacing
col_diameter = 0.8 # m
col_spacing = 1.5 # m

# compute area replacement ratio
a_s = calc_area_repl_ratio(col_diameter, col_spacing, True)

# message
print(f'\n3. Collect granular columns data')
print(f'column diameter            = {col_diameter} m')
print(f'column spacing             = {col_spacing} m')
print(f'area replacement ratio a_s = {a_s:.2f}')

# 4. Compute bearing capacity of single granular column ##################

# use simplified formula
qult_col = 20.0 * soil_cu # kPa

# message
print(f'\n4. Compute bearing capacity of single granular column')
print(f'qult (column) = {qult_col} kPa')

# 5. Compute bearing capacity of natural ground ##########################

# compute shape factors
Bf = foot_width # m
Lf = foot_width # m
Df = foot_depth # m
shape_factor_sc = 1.0 + 0.2 * Bf / Lf
shape_factor_dc = 1.0 + 0.2 * Df / Bf

# set N coefficients
Nc = 5.14
Nq = 1.0

# compute bearing capacity of soil
qult_soil = soil_cu * Nc * shape_factor_sc * shape_factor_dc + sig_overb_eff * Nq

# message
print(f'\n5. Compute bearing capacity of natural ground')
print(f'shape factor sc = {shape_factor_sc}')
print(f'shape factor dc = {shape_factor_dc}')
print(f'qult (soil)     = {qult_soil:.1f} kPa')

# 6. Compute bearing capacity of composite foundation ####################

# bearing capacity of composite foundation
qult = qult_col * a_s + qult_soil * (1.0 - a_s)

# message
print(f'\n6. Compute bearing capacity of composite foundation')
print(f'qult = {qult:.1f} kPa')

# 7. Check factor of safety ############################################

# compute factor of safety
FS = qult / pressure
FS_required = 2.5

# message
print(f'\n7. Check factor of safety')
print(f'FS = {FS:.2f}')
if FS < FS_required:
    print(f'This design does not meet the bearing capacity requirement')
else:
    print('OK')

# 8. Modify the design #################################################

# compute the required bearing capacity
qult_req = FS_required * pressure

# compute the new area replacement ratio
as_new_temp = (qult_req - qult_soil) / (qult_col - qult_soil)

# compute and select the new spacing
C = pi / (2.0 * sr3)
s_new_temp = col_diameter / np.sqrt( as_new_temp / C )
s_new = 1.2

# recompute the new area replacement ratio
as_new = calc_area_repl_ratio(col_diameter, s_new, True)

# compute the new bearing capacity of the composite foundation
qult_new = qult_col * as_new + qult_soil * (1.0 - as_new)

# check the new factor of safety
FS_new = qult_new / pressure

# message
print(f'\n8. Modify the design')
print(f'new: qult_req           = {qult_req} kPa')
print(f'new: a_s (temp)         = {as_new_temp:.2f}')
print(f'new: spacing (computed) = {s_new_temp:.2f} m')
print(f'new: spacing (selected) = {s_new:.2f} m')
print(f'new: a_s                = {as_new:.2f}')
print(f'new: qult               = {qult_new:.1f} kPa')
print(f'new: FS                 = {FS_new:.2f}')
if FS_new < FS_required:
    print(f'This design does not meet the bearing capacity requirement')
else:
    print('OK')
