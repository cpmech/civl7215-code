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
aux1 = (0.23 + 0.06 / D50) ** 1.7
aux2 = (100.0 / sigma_z0_eff) ** 0.5
Dr = 100.0 * ( (N60 * aux1 / 9.0) * aux2 ) ** 0.5

# corrected SPT value
N1_60 = N60 * np.sqrt(100.0 / sigma_z0_eff)

# message
print(f'\nDr  = {Dr:.0f} [%]')
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
print(f'\nMSF = {MSF:.2f}')
print(f'CRR = {CRR:.3f}')

