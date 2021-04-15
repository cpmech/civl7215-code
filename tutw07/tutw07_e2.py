import numpy as np

'''
INPUT
  40 m wideand 1.8 m high embankment (fill)
  5 m thick soft clay on top of stiffer clay
  using a 0.3 m thick fill for drainage on the surface
  groundwater table is 1 m below surface
FILL
  fill unit weight = 18 kN/m3
SOFT CLAY
  gamma = 15 kN/m3, Es = 1.1 MPa
  kr = 3.47e-9 m/s, kv = 1.16e-9 m/s
STONE COLUMNS
  diameter of 0.8 m and 6 m long
  square pattern with spacing equal to 2.4 m
  dry unit weight = 15.7 kN/m3
  specific gravity = 2.70
  elastic modulus = 30 MPa
  Poisson ratio = 0.3
  columns have 20% clay particles with D10 = 0.005 mm
OUTPUT
  Settlement without stone columns
  Settlement with stone columns
  Consolidation settlement of composite foundation at one month
  Assume instantaneous placement of embankment
'''

# some constants
gw = 9.81 # kN/m³ unit weight of water
pi = np.pi # 3.14159...
sr2 = np.sqrt(2.0)
sr3 = np.sqrt(3.0)
seconds_per_day = 24.0 * 60.0 * 60.0

# function to compute the area replacement ratio
def calc_area_repl_ratio(dc, s, triangular_pattern = False):
    C = pi / (2.0 * sr3) if triangular_pattern else pi / 4.0
    return C * (dc / s) ** 2.0

# function to approximate the average degree of vertical consolidation (Terzaghi)
def consolid_calc_Uv_given_Tv(Tv):
    if Tv <= 0.217:
        return 2.0 * np.sqrt(Tv / np.pi)
    else:
        a = (1.781 - Tv) / 0.933
        return 1.0 - (10.0 ** a) / 100.0

# function to approximate the degree of consolidation due to radial flow (Barron)
def consolid_calc_Ur_given_Tr(Tr, Nd):
    aux = Nd ** 2.0
    Fnd = np.log(Nd) * aux / (aux - 1.0) - (3.0*aux - 1.0) / (4.0*aux)
    return 1.0 - np.exp(-8.0 * Tr / Fnd)

# 1. Collect fill data #########################################################

# height of embankment and unit weight of embankment
hf = 1.8 # m
gf = 18.0 # kN/m³

# additional vertical stress due to fill (immediate) construction
Dsigz = hf * gf # kPa

# message
print(f'\n1. Collect fill data')
print(f'Dsigz = {Dsigz} kPa')

# 2. Collect soft clay data ####################################################

# unit weight (gs), soil modulus (Es), radial permeability (kr), and vertical permeability (kv)
gs = 15.0 # kN/m³
Es = 1.1 * 1000.0 # kPa
kr = 3.47e-9 # m/s
kv = 1.16e-9 # m/s

# assume Poisson ratio of soft soil (e.g. 0.3)
nus = 0.3

# height of clay layer
h = 5.0 # m

# compute coefficient of volume compressibility of natural soil (mvs)
mvs = (1.0 + nus) * (1.0 - 2.0*nus) / (Es*(1.0 - nus))

# compute coefficient of consolidation due to vertical flow (cv)
cv = kv / (gw * mvs)

# compute coefficient of consolidation due to radial flow (cr)
cr = kr / (gw * mvs)

# message
print(f'\n2. Collect soft clay data')
print(f'mvs = {mvs:.6f} kPa⁻¹')
print(f'cv  = {cv:.2e} m²/s')
print(f'cr  = {cr:.2e} m²/s')

# 3. Collect stone columns data ################################################

# diameter (dc), length (Lc), spacing (s), unit weight (gc), modulus (Ec) and Poisson (nuc)
dc = 0.8 # m
Lc = 6.0 # m
s = 2.4 # m
gc = 15.7 # kN/m³
Ec = 30.0 * 1000.0 # kPa
nuc = 0.3

# specific gravity of column (Gs_col)
Gs_col = 2.70

# clay particles in column (D10 and P200)
D10 = 0.005 # mm
P200 = 20 # %

# porosity of stone column (por_col)
por_col = 1.0 - gc / (gw * Gs_col)

# permeability of stone column (kc)
kc = 2.19 * (D10**1.478) * (por_col**6.654) / (P200**0.597)

# message
print(f'\n3. Collect stone columns data')
print(f'por_col = {por_col:.3f}')
print(f'kc      = {kc:.2e} m/s')

# 4. Compute settlement without stone columns ##################################

# compute S
S = mvs * Dsigz * h
print(f'\n4. Compute settlement without stone columns')
print(f'S = {S*1000:.0f} mm')

# 5. Compute stress reduction factor (mu) ######################################

# area replacement ratio
a_s = calc_area_repl_ratio(dc, s, False)

# modulus ratio of column to soil
modulus_ratio_calc = Ec / Es

# check modulus ratio (must be ≤ 20)
modulus_ratio = 20.0 if modulus_ratio_calc > 20.0 else modulus_ratio_calc

# stress concentration ratio
n_calc = 1.0 + 0.217 * (modulus_ratio - 1.0)

# check stress concentration ratio (must be ≤ 5)
n = 5.0 if n_calc > 5.0 else n_calc

# compute stress reduction factor (mu)
mu = 1.0 / (1.0 + a_s * (n - 1.0))

# message
print(f'\n5. Compute stress reduction factor (mu)')
print(f'area repl ratio a_s         = {a_s:.3f}')
print(f'modulus ratio (calc)        = {modulus_ratio_calc:.2f}')
print(f'modulus ratio (final)       = {modulus_ratio:.2f}')
print(f'stress conc ratio n (calc)  = {n_calc:.2f}')
print(f'stress conc ratio n (final) = {n:.2f}')
print(f'stress reduction factor mu  = {mu:.3f}')

# 6. Settlement with stone columns #############################################

# compute settlement with stone columns
S_composite = mu * S

# message
print(f'\n6. Settlement with stone columns')
print(f'S (composite) = {S_composite*1000:.0f} mm')

# 7. Compute modified coefficients of consolidation ############################

# equivalent diameter of unit cell (de)
de = 2.0 * s / np.sqrt(pi)

# diameter ratio (Nd)
Nd = de / dc

# auxiliary multiplier
multiplier = (1.0 + n / (Nd**2.0 - 1.0))

# modified coefficient of consolidation due to vertical flow (cvm)
cvm = cv * multiplier

# modified coefficient of consolidation due to radial flow (crm)
crm = cr * multiplier

# message
print(f'\n7. Compute modified coefficients of consolidation')
print(f'de  = {de:.1f} m')
print(f'Nd  = {Nd:.1f}')
print(f'cvm = {cvm:.2e} m²/s')
print(f'crm = {crm:.2e} m²/s')

# 8. Compute time factors ######################################################

# convert time to seconds (t)
t_days = 30 # days => one month after the construction of the embankment
t = t_days * seconds_per_day # seconds

# vertical drainage path (note that the underlain stiff clay has low permeability) (hdr)
hdr = h # m

# time factor due to vertical flow (Tv)
Tv = cvm * t / hdr**2.0

# time factor due to radial flow (Tr)
Tr = crm * t / de**2.0

# message
print(f'\n8. Compute time factors')
print(f'hdr = {h} m')
print(f'Tv  = {Tv:.3f}')
print(f'Tr  = {Tr:.3f}')

# 9. Degree of consolidation ###################################################

# degree of consolidation due to the vertical flow according to Terzaghi's (Uv)
Uv = consolid_calc_Uv_given_Tv(Tv)

# degree of consolidation due to the radial flow according to Barron's solution (Ur)
Ur = consolid_calc_Ur_given_Tr(Tr, Nd)

# degree of consolidation due to combined vertical and radial flow (Uvr)
Uvr = 1.0 - (1.0 - Uv) * (1.0 - Ur)

# message
print(f'\n9. Degree of consolidation')
print(f'Uv  = {Uv:.3f}')
print(f'Ur  = {Ur:.3f}')
print(f'Uvr = {Uvr * 100:.2f} %')

# 10. Consolidation settlement of composite foundation #########################

# compute consolidation after 1 month
St = Uvr * S_composite

# message
print(f'\n10. Consolidation settlement of composite foundation')
print(f'St = {St*1000:.0f} mm')
