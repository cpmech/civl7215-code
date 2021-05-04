import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

# 1. Set up some constants #########################################################################

# pi, unit weight of water, and number of seconds in day
pi = np.pi # [-]
gamma_water = 9.8 # kN/m³
secs_per_day = 24 * 60 * 60.0 # [-]
 
# 2. Soil foundation data ##########################################################################
 
# Thickness of clay layer, OCR, undrained strength
H_soil = 6.0 # m
OCR_soil = 1.0 # normally consolidated
cu_soil = 24.0 # kPa

# Coefficient of consolidation due to vertical flow
cv_soil = 1.8e-8 # m²/s

# Coefficient of consolidation due to radial flow
cr_soil = 2.5 * cv_soil

# Compression index and secondary compression index
Cc_soil = 0.8 # [-]
Ca_soil = 0.032 # [-]

# Initial void ratio, unit weight, effective unit weight
e0_soil = 1.0 # [-]
gamma_soil = 18.1 # kN/m³
egamma_soil = gamma_soil - gamma_water # effective unit weight

# Estimate the coefficient of 1D compressibility
esigA = 100.0 # kPa
esigB = 200.0 # kPa
mv_soil = (Cc_soil / (1.0 + e0_soil)) * np.log10(esigB / esigA) / (esigB - esigA)

# Compute the vertical permeability from mv
kv_soil = cv_soil * mv_soil * gamma_water

# Compute the radial permeability from kv
kr_soil = 2.5 * kv_soil

# message
print(f'\n2. Soil foundation data')
print(f'H      = {H_soil} m')
print(f'OCR    = {OCR_soil} [-]')
print(f'cu     = {cu_soil} kPa')
print(f'cv     = {cv_soil} m²/s')
print(f'cr     = {cr_soil} m²/s')
print(f'Cc     = {Cc_soil} [-]')
print(f'Ca     = {Ca_soil} [-]')
print(f'e0     = {e0_soil} [-]')
print(f'gamma  = {gamma_soil} kN/m³')
print(f'egamma = {egamma_soil} kN/m³')
print(f'mv     = {mv_soil:.6f} kPa⁻¹')
print(f'kv     = {kv_soil:.4} m/s')
print(f'kr     = {kr_soil:.4} m/s')

# 3. Embankment (fill) data ########################################################################

# Height of fill, unit weight, effective cohesion, and effective friction angle
H_fill = 6.0 # m
gamma_fill = 19.7 # kN/m³
c_fill = 0.0 # kPa
phi_fill = 30.0 # °

# message
print(f'\n3. Embankment (fill) data')
print(f'H     = {H_fill} m')
print(f'gamma = {gamma_fill} kN/m³')
print(f'c     = {c_fill} kPa')
print(f'phi   = {phi_fill} °')

# 4. Pre-fabricated drains (PVD) ###################################################################

# Width (b) and thickness (tg)
b_drain = 100.0 # mm
tg_drain = 4.0 # mm

# Spacing and discharge capacity (Qc)
spacing_drain = 1.0 # m (equilateral triangular pattern)
Qc_drain = 0.000109 # m3/s

# Compute the equivalent diameter of drain (dc)
dc_drain = (b_drain/1000.0 + tg_drain/1000.0) / 2

# Compute the equivalent influence diameter (de)
de_drain = 1.06 * spacing_drain

# Compute the diameter ratio (Nd)
Nd_drain = de_drain / dc_drain

# message
print(f'\n4. Pre-fabricated drains (PVD)')
print(f'equivalent diameter of drain:  dc = {dc_drain:.4f} m')
print(f'equivalent influence diameter: de = {de_drain} m')
print(f'diameter ratio:                Nd = {Nd_drain:.2f}')

# 5. Geotechnical problem ##########################################################################

# Factor of safety for bearing capacity
FS_bearing_cap = 1.3 # [-]

# Drainage length (hdr)
hdr_soil = 6.0 # m (thickness of clay layer)

# Depth of middle of the clay layer
z_soil = 3.0 # m (middle of clay layer)

# Assume construction rate (e.g. 0.3 m / week)
construct_rate_w = 0.3 # m/week
construct_rate = construct_rate_w / 7.0 # m/day

# Compute auxiliary coefficients bv and br
bv = cv_soil / (hdr_soil**2)
br = cr_soil / (de_drain**2)

# Compute the Fm(Nd) coefficient for the radial flow equation
aux = pi * z_soil * (2*hdr_soil - z_soil) * kr_soil / Qc_drain
Fm = np.log(Nd_drain) - 0.75 + aux

# message
print(f'\n5. Geotechnical problem')
print(f'FS           = {FS_bearing_cap} [-]')
print(f'hdr          = {hdr_soil} m')
print(f'z            = {z_soil} m')
print(f'construction = {construct_rate:.6f} m/day')
print(f'bv           = {bv:.2e} [-]')
print(f'br           = {br:.2e} [-]')
print(f'Fm           = {Fm:.2f}')

# 6. Functions #####################################################################################

# Define a function to calculate Uv
def calc_Uv(tau):
    Tv = bv * tau
    if Tv <= 0.217: return 2.0 * np.sqrt(Tv / np.pi)
    return 1.0 - 10.0**(-(Tv + 0.085)/0.933)

# Define a function to calculate Ur
def calc_Ur(tau):
    Tr = br * tau
    return 1.0 - np.exp(-8.0*Tr/Fm)

# Define a function to calculate Uvr
def calc_Uvr(Uv, Ur):
    return 1.0 - (1.0 - Uv) * (1.0 - Ur)

# Define a function to calculate the residual from Uvr and the fixed 80% value
def calc_resid_one(tau):
    Uvr_fixed = 0.8
    Uv = calc_Uv(tau)
    Ur = calc_Ur(tau)
    return Uvr_fixed - 1.0 + (1.0-Uv) * (1.0-Ur)
calc_resid_vector = np.vectorize(calc_resid_one)

# 7. Maximum fill height ###########################################################################

# Compute the allowed pressure based on the foundation undrained strength
p_allowed = 5.14 * cu_soil / FS_bearing_cap

# Compute the maximum allowed height of fill
H_max_calc = p_allowed / gamma_fill

# Round down maximum fill height
H_max = 4.5 # m

# message
print(f'\n7. Maximum fill height')
print(f'allowed p   = {p_allowed:.2f} kPa')
print(f'Hmax (calc) = {H_max_calc:.2f} m')
print(f'Hmax        = {H_max} m')
 
# 8. Total primary settlement ######################################################################

# Compute the total stress increment
dsigz = gamma_fill * H_max # kPa

# Set the effective stress increment
desigz = dsigz # delta effective vertical stress

# Compute the initial and final effective stresses at the mid-depth of the soft soil
esigz_ini = egamma_soil * z_soil
esigz_fin = esigz_ini + desigz

# Compute the total primary settlement
S_total = H_soil * Cc_soil * np.log10(esigz_fin / esigz_ini) / (1.0 + e0_soil)

# message
print(f'\n8. Total primary settlement')
print(f'dsigz     = {dsigz:.2f} kPa')
print(f'desigz    = {desigz:.2f} kPa')
print(f'esigz_ini = {esigz_ini:.2f} kPa')
print(f'esigz_fin = {esigz_fin:.2f} kPa')
print(f'S_total   = {S_total:.2f} m')
 
# 9. Data for the first loading stage ##############################################################

# Choose height of the fill for the first loading stage
H1 = 4.5 # m

# Compute the time period for the construction of the first stage
period1_calc = np.ceil(H1 / construct_rate) # day

# Round-up the number of days
period1 = np.ceil(period1_calc) # day

# Compute the time at the beginning and at the end of construction, and the shift-time for Stage 1
t1ini = 0.0
t1fin = t1ini + period1 * secs_per_day
dt1 = (t1ini + t1fin) / 2.0
tau1_t1fin = t1fin - dt1

# message
print(f'\n9. Data for the first loading stage')
print(f'height of fill        = {H1} m')
print(f'construction time     = {period1} days')
print(f'time at the beginning = {t1ini/secs_per_day} days')
print(f'time at the end of    = {t1fin/secs_per_day} days')

# 10. Consolidation settlement at the end of construction (Stage 1) ################################

# Compute the degrees of consolidation due to Stage 1 at the end of construction of Stage 1
Uv1_t1fin = calc_Uv(tau1_t1fin)
Ur1_t1fin = calc_Ur(tau1_t1fin)
Uvr1_t1fin = calc_Uvr(Uv1_t1fin, Ur1_t1fin)

# Compute the excess pore water pressure due to Stage 1 at the end of construction of Stage 1
u1_ini = H1 * gamma_fill
u1_t1fin = u1_ini * (1.0 - Uvr1_t1fin)

# Compute the consolidation settlement at the end of construction of Stage 1
S_t1fin = Uvr1_t1fin * S_total

# message
print(f'\n10. Consolidation settlement at the end of construction (Stage 1)')
print(f'Uv  @ t1fin = {Uv1_t1fin*100:.2f} %')
print(f'Ur  @ t1fin = {Ur1_t1fin*100:.2f} %')
print(f'Uvr @ t1fin = {Uvr1_t1fin*100:.2f} %')
print(f'u1  @ t1ini = {u1_ini:.2f} kPa')
print(f'u1  @ t1fin = {u1_t1fin:.2f} kPa')
print(f'S   @ t1fin = {S_t1fin:.2f} m')


# 11. Consolidation settlement at the end of the waiting period (Stage 1) ##########################

# Find $\tau$ such that 80% consolidation (Uvr = 0.8) has occurred
# Compute time $t$ from the the time-shift $\tau$
# Round-up the number of days
# Check if the overall degree of consolidation is close to 80%
# Compute the excess pore-water pressure
# Compute the consolidation settlement

# 12. Strength gain ################################################################################

# Compute the strength gain due to consolidation at the end of the wait time of Stage 1

# 13. Revised maximum fill height ##################################################################

# Compute the allowed pressure based on the updated foundation undrained strength
# Compute the maximum allowed height of fill
# Round down maximum fill height

# 14. Revised total primary settlement #############################################################

# Compute the total stress increment
# Compute the initial and final effective stresses at the mid-depth of the soft soil
# Compute the total primary settlement

# 15. Data for the second loading stage ############################################################

# Choose height of the fill for the second loading stage
# Compute the time period for the construction of the second stage
# Round-up the number of days
# Compute the time at the beginning and at the end of construction, and the shift-time for Stage 2
 
# 17. Consolidation settlement at the end of construction (Stage 2) ################################

# Compute the degrees of consolidation due to Stage 1 at the end of construction of Stage 2
# Compute the degrees of consolidation due to Stage 2 at the end of construction of Stage 2
# Compute the excess pore water pressure due to Stage 1 at the end of construction of Stage 2
# Compute the excess pore water pressure due Stage 2 at the end of construction of Stage 2
# Compute the overall degree of consolidation due to Stage 1 and Stage 2
# Compute the consolidation settlement at the end of construction of Stage 2

# 18. Consolidation settlement at the end of the waiting period (Stage 2) ##########################

# Set time at the end of the wait period of Stage 2 as the final allowed time (1 year)
# Compute $\tau$ at the final time
# Compute the degrees of consolidation due to Stage 1 at the end of wait time of Stage 2
# Compute the degrees of consolidation due to Stage 2 at the end of wait time of Stage 2
# Compute the excess pore water pressure due to Stage 1 at the end of wait time of Stage 2
# Compute the excess pore-water pressure due Stage 2 at the end of wait time of Stage 2
# Compute the overall degree of consolidation due to Stage 1 and Stage 2
# Compute the consolidation settlement at the end of the wait time of Stage 2

# 19. Post-construction settlement #################################################################

# Compute the remaining settlement
# Find $t$ corresponding to 99% consolidation (Uvr = 0.99)
# Compute the settlement due to traffic loading
# Compute the secondary settlement
# Compute the post-construction settlement
 
# 20. Plots ########################################################################################

# Plot the fill height versus time
# Plot the settlement versus time
# Plot the excess pore water pressure due to the first embankment
# Plot the excess pore water pressure due to the second embankment
