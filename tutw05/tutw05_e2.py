import numpy as np

'''
KNOWN
  * Uniform medium sand with 5% fine content
  * Thickness of sand layer = 12 m
  * eMin = 0.45, eMax = 0.98
  * Groundwater table @ 1.5 m from the surface
  * SPT: N60=5 @ 6m (low)
  * Seismicity expected => liquefaction potential
  * Earthquake magnitute ~ 7.0
  * Peak ground acceleration ~ 0.3 g
  * Average column diameter ~ 0.8 m
  * Length of granular columns = 12 m
  * Ground subsidence = 50 mm
REQUIRED
  * Spacing of columns (square pattern)
  * Eliminate liquefaction potential
'''

# 0 Define Equation 2.33 #################################################

def Dr_from_SPT(d50, n60, s0eff):
    aux1 = (0.23 + 0.06 / d50) ** 1.7
    aux2 = (100.0 / s0eff) ** 0.5
    dr = ( (n60 * aux1 / 9.0) * aux2 ) ** 0.5
    return dr * 100.0 # %

# 1 Estimate soil data ###################################################

# assume unit weights of sand (below and above water table)
gamma_dry = 19.0 # kN/m³
gamma_sat = 20.0 # kN/m³

# assume particle sizes (using ASTM)
# for medium sand:
# min particle size = 0.425 mm (No. 40)
# max particle size = 2.00 mm (No. 10)
# thus, we can assume:
D50 = 1.2 # mm

# message
print(f'\n1 Estimate soil data')
print(f'gamma_dry = {gamma_dry} kN/m³')
print(f'gamma_sat = {gamma_sat} kN/m³')
print(f'D50       = {D50} mm')

# 2 Effective overburden stress ##########################################

# consider middle of layer:
z_middle = 6.0 # meters
z_watertable = 1.5 # meters

# compute the total and effective stresses
h_dry = z_watertable # m
h_wet = z_middle - z_watertable # m
sigma_z0 = gamma_dry * h_dry + gamma_sat * h_wet # kPa
sigma_z0_eff = gamma_dry * h_dry + (gamma_sat - 9.81) * h_wet # kPa

# message
print(f'\n2 Effective overburden stress')
print(f'h_dry        = {h_dry:.1f} [m]')
print(f'h_wet        = {h_wet:.1f} [m]')
print(f'sigma_z0     = {sigma_z0:.1f} [kPa]')
print(f'sigma_z0_eff = {sigma_z0_eff:.1f} [kPa]')

# 3 Relative density and SPT value #######################################

# given data
e_min = 0.45
e_max = 0.98
N60 = 5.0

# use Equation 2.33 to estimate Dr
N60 = 5 # SPT value
Dr = Dr_from_SPT(D50, N60, sigma_z0_eff)

# corrected SPT value
N1_60 = N60 * np.sqrt(100.0 / sigma_z0_eff)

# message
print(f'\n3 Relative density and SPT value')
print(f'Dr    = {Dr:.0f} [%]')
print(f'N1_60 = {N1_60:.1f}')

# 4 Cyclic resistance ratio ##############################################

# moment magnitude of the earthquake
Mw = 7.0

# magnitude scaling factor (MSF)
MSF = 1.82 if Mw < 5.2 else 6.9 * np.exp(-Mw/4.0) - 0.06

# cyclic resistance ratio (CRR_M75) for earthquake magnitude 7.5
# use Figure 2.83 to estimate CRR_M75 using N1_60
CRR_M75 = 0.06

# cyclic resistance ratio (CRR)
CRR = MSF * CRR_M75

# message
print(f'\n4 Cyclic resistance ratio')
print(f'MSF = {MSF:.2f}')
print(f'CRR = {CRR:.3f}')

# 5 Liquefaction factor of safety ########################################

# use Figure 2.82 to estimate rd using depth = z_middle
rd = 0.96

# set acceleration ratio, considering 0.3g / g
accel_ratio = 0.3

# compute the cyclic stress ratio CSR
CSR = 0.65 * rd * (sigma_z0 / sigma_z0_eff) * accel_ratio

# compute factor of safety against liquefaction
FS = CRR / CSR

# message
print(f'\n5 Liquefaction factor of safety')
print(f'CSR              = {CSR:.4f}')
print(f'FS               = {FS:.2f}')
print(f'FS: satisfactory = {FS > 1}')

# 6 Vibro-compaction: improved FS, CRR and N60 ###########################

# specify factor of safety for after the ground improvement
FS_new = 1.2

# compute improved CRR and CRR_M75
CRR_new = FS_new * CSR
CRR_M75_new = CRR_new / MSF

# use Figure 2.83 to estimate N1_60 using CRR_M75
N1_60_new = 26.0

# compute improved N60
N60_new = N1_60_new / np.sqrt(100.0/sigma_z0_eff)

print(f'\n6 Vibro-compaction: improved FS, CRR and N60')
print(f'FS      (new) = {FS_new}')
print(f'CRR     (new) = {CRR_new:.4f}')
print(f'CRR_M75 (new) = {CRR_M75_new:.4f}')
print(f'N60     (new) = {N60_new:.1f}')

# 7 Spacing for vibro-compaction improvement #############################

# required relative density
Dr_new = Dr_from_SPT(D50, N60_new, sigma_z0_eff)

# initial void ratio
e0 = e_max - (Dr/100.0) * (e_max- e_min)

# final void ratio
e1 = e_max - (Dr_new/100.0) * (e_max - e_min)

# given data
Cg = 0.89 # # granular columns in square pattern
dcl = 0.8 # m, diameter of column
h = 12.0 # m, improvement depth
S = 50.0 / 1000.0 # m, expected ground subsidence

# compute spacing
aux = (1.0 + e0) * h / ((e0 - e1) * h - (1.0 + e0) * S)
s = Cg * dcl * np.sqrt(aux)

# message
print(f'\n7 Spacing for vibro-compaction improvement')
print(f'Dr (new)   = {Dr_new:.0f} %')
print(f'e0         = {e0:.3f}')
print(f'e1         = {e1:.3f}')
print(f'spacing: s = {s:.1f} m')
