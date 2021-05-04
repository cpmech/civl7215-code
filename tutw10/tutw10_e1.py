import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

# 0. Set up some constants #########################################################################

# pi, unit weight of water, and number of seconds in day
pi = np.pi # [-]
gamma_water = 9.8 # kN/m³
secs_per_day = 24 * 60 * 60.0 # [-]
 
# 1. Soil foundation data ##########################################################################
 
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
print(f'\n1. Soil foundation data')
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

# 2. Embankment (fill) data ########################################################################

# Height of fill, unit weight, effective cohesion, and effective friction angle
H_fill = 6.0 # m
gamma_fill = 19.7 # kN/m³
c_fill = 0.0 # kPa
phi_fill = 30.0 # °

# message
print(f'\n2. Embankment (fill) data')
print(f'H     = {H_fill} m')
print(f'gamma = {gamma_fill} kN/m³')
print(f'c     = {c_fill} kPa')
print(f'phi   = {phi_fill} °')

# 3. Pre-fabricated drains (PVD) ###################################################################

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
print(f'\n3. Pre-fabricated drains (PVD)')
print(f'dc = {dc_drain:.4f} m')
print(f'de = {de_drain} m')
print(f'Nd = {Nd_drain:.2f}')

# 4. Geotechnical problem ##########################################################################

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
print(f'\n4. Geotechnical problem')
print(f'FS           = {FS_bearing_cap} [-]')
print(f'hdr          = {hdr_soil} m')
print(f'z            = {z_soil} m')
print(f'construction = {construct_rate:.6f} m/day')
print(f'bv           = {bv:.2e} [-]')
print(f'br           = {br:.2e} [-]')
print(f'Fm           = {Fm:.2f}')

# 5. Functions #####################################################################################

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

# message
print(f'\n5. Functions')
print('done')

# 6. Maximum fill height ###########################################################################

# Compute the allowed pressure based on the foundation undrained strength
p_allowed = 5.14 * cu_soil / FS_bearing_cap

# Compute the maximum allowed height of fill
H_max_calc = p_allowed / gamma_fill

# Round down maximum fill height
H_max = 4.5 # m

# message
print(f'\n6. Maximum fill height')
print(f'allowed p   = {p_allowed:.2f} kPa')
print(f'Hmax (calc) = {H_max_calc:.2f} m')
print(f'Hmax        = {H_max} m')
 
# 7. Total primary settlement ######################################################################

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
print(f'\n7. Total primary settlement')
print(f'desigz    = {desigz:.2f} kPa')
print(f'esigz_ini = {esigz_ini:.2f} kPa')
print(f'esigz_fin = {esigz_fin:.2f} kPa')
print(f'S_total   = {S_total:.2f} m')
 
# 8. Data for the first loading stage ##############################################################

# Choose height of the fill for the first loading stage
H1 = 4.5 # m

# Compute the time period for the construction of the first stage
period1_calc = H1 / construct_rate # day

# Round-up the number of days
period1 = np.ceil(period1_calc) # day

# Compute the time at the beginning and at the end of construction, and the shift-time for Stage 1
t1ini = 0.0 # secs
t1fin = t1ini + period1 * secs_per_day # secs
dt1 = (t1ini + t1fin) / 2.0 # secs
tau1_t1fin = t1fin - dt1 # secs

# message
print(f'\n8. Data for the first loading stage')
print(f'height of fill, H1    = {H1} m')
print(f'construction time     = {period1} days')
print(f'time at the beginning = {t1ini/secs_per_day} days')
print(f'time at the end of    = {t1fin/secs_per_day} days')

# 9. Consolidation settlement at the end of construction (Stage 1) #################################

# Compute the degrees of consolidation due to Stage 1 at the end of construction of Stage 1
Uv1_t1fin = calc_Uv(tau1_t1fin)
Ur1_t1fin = calc_Ur(tau1_t1fin)
Uvr1_t1fin = calc_Uvr(Uv1_t1fin, Ur1_t1fin)

# Compute the excess pore water pressure due to Stage 1 at the end of construction of Stage 1
u1_t1ini = H1 * gamma_fill
u1_t1fin = u1_t1ini * (1.0 - Uvr1_t1fin)

# Compute the consolidation settlement at the end of construction of Stage 1
S_t1fin = Uvr1_t1fin * S_total

# message
print(f'\n9. Consolidation settlement at the end of construction (Stage 1)')
print(f't1fin                    = {t1fin/secs_per_day} days')
print(f'Uv    of stage 1 @ t1fin = {Uv1_t1fin*100:.2f} %')
print(f'Ur    of stage 1 @ t1fin = {Ur1_t1fin*100:.2f} %')
print(f'Uvr   of stage 1 @ t1fin = {Uvr1_t1fin*100:.2f} %')
print(f'u1 due to load 1 @ t1ini = {u1_t1ini:.2f} kPa')
print(f'u1 due to load 1 @ t1fin = {u1_t1fin:.2f} kPa')
print(f'S  due to load 1 @ t1fin = {S_t1fin:.2f} m')

# 10. Consolidation settlement at the end of the waiting period (Stage 1) ##########################

# Find tau such that 80% consolidation (Uvr = 0.8) has occurred
tau1_tlong = tau1_t1fin + 365 * secs_per_day
tau1_t1wait = opt.brentq(calc_resid_vector, tau1_t1fin, tau1_tlong)

# Compute time t from the the time-shift tau
t1wait_calc = tau1_t1wait + dt1 # secs

# Round-up the number of days
t1wait_days = np.ceil(t1wait_calc/secs_per_day) # days
t1wait = t1wait_days * secs_per_day # secs

# Recompute the overall degree of consolidation after the rounding up
tau1_t1wait = t1wait - dt1
Uv1_t1wait = calc_Uv(tau1_t1wait)
Ur1_t1wait = calc_Ur(tau1_t1wait)
Uvr1_t1wait = calc_Uvr(Uv1_t1wait, Ur1_t1wait)

# Compute the excess pore-water pressure
u1_t1wait = u1_t1ini * (1.0 - Uvr1_t1wait)

# Compute the consolidation settlement
S_t1wait = Uvr1_t1wait * S_total

# message
print(f'\n10. Consolidation settlement at the end of the waiting period (Stage 1)')
print(f't1wait                    = {t1wait/secs_per_day} days')
print(f'Uv    of stage 1 @ t1wait = {Uv1_t1wait*100:.2f} %')
print(f'Ur    of stage 1 @ t1wait = {Ur1_t1wait*100:.2f} %')
print(f'Uvr   of stage 1 @ t1wait = {Uvr1_t1wait*100:.2f} %')
print(f'u1 due to load 1 @ t1wait = {u1_t1wait:.2f} kPa')
print(f'S  due to load 1 @ t1wait = {S_t1wait:.2f} m')

# 11. Strength gain ################################################################################

# Compute the strength gain due to consolidation at the end of the wait time of Stage 1
dcu1 = 0.25 * Uvr1_t1wait * dsigz

# message
print(f'\n11. Strength gain')
print(f'dcu due to stage 1 @ t1_wait = {dcu1:.2f} kPa')

# 12. Revised maximum fill height ##################################################################

# Compute the allowed pressure based on the updated foundation undrained strength
p_allowed = 5.14 * (cu_soil + dcu1) / FS_bearing_cap

# Compute the maximum allowed height of fill
H_max_calc = p_allowed / gamma_fill

# Round down maximum fill height
H_max = 8.0 # m

# message
print(f'\n12. Revised maximum fill height')
print(f'allowed p   = {p_allowed:.2f} kPa')
print(f'Hmax (calc) = {H_max_calc:.2f} m')
print(f'Hmax        = {H_max} m')

# 13. Revised total primary settlement #############################################################

# Compute the total stress increment
dsigz = gamma_fill * H_max

# Compute the initial and final effective stresses at the mid-depth of the soft soil
desigz = dsigz # delta effective vertical stress
esigz_ini = egamma_soil * z_soil
esigz_fin = esigz_ini + desigz

# Compute the total primary settlement
S_total = H_soil * Cc_soil * np.log10(esigz_fin / esigz_ini) / (1.0 + e0_soil)

# message
print(f'\n13. Revised total primary settlement')
print(f'desigz    = {desigz:.2f} kPa')
print(f'esigz_ini = {esigz_ini:.2f} kPa')
print(f'esigz_fin = {esigz_fin:.2f} kPa')
print(f'S_total   = {S_total:.2f} m')

# 14. Data for the second loading stage ############################################################

# Choose height of the fill for the second loading stage
H2 = H_max - H1

# Compute the time period for the construction of the second stage
period2_calc = H2 / construct_rate # day

# Round-up the number of days
period2 = np.ceil(period2_calc) # day

# Compute the time at the beginning and at the end of construction, and the shift-time for Stage 2
t2ini = t1wait # secs
t2fin = t2ini + period2 * secs_per_day # secs
dt2 = (t2ini + t2fin) / 2.0 # secs
tau2_t2fin = t2fin - dt2 # secs

# message
print(f'\n14. Data for the second loading stage')
print(f'height of fill, H2    = {H2} m')
print(f'construction time     = {period2} days')
print(f'time at the beginning = {t2ini/secs_per_day} days')
print(f'time at the end of    = {t2fin/secs_per_day} days')
 
# 15. Consolidation settlement at the end of construction (Stage 2) ################################

# Compute the degrees of consolidation due to Stage 1 at the end of construction of Stage 2
tau1_t2fin = t2fin - dt1
Uv1_t2fin = calc_Uv(tau1_t2fin)
Ur1_t2fin = calc_Ur(tau1_t2fin)
Uvr1_t2fin = calc_Uvr(Uv1_t2fin, Ur1_t2fin)

# Compute the degrees of consolidation due to Stage 2 at the end of construction of Stage 2
Uv2_t2fin = calc_Uv(tau2_t2fin)
Ur2_t2fin = calc_Ur(tau2_t2fin)
Uvr2_t2fin = calc_Uvr(Uv2_t2fin, Ur2_t2fin)

# Compute the excess pore water pressure due to Stage 1 at the end of construction of Stage 2
u1_t2fin = u1_t1ini * (1.0 - Uvr1_t2fin)

# Compute the excess pore water pressure due Stage 2 at the end of construction of Stage 2
u2_t2ini = H2 * gamma_fill
u2_t2fin = u2_t2ini * (1.0 - Uvr2_t2fin)

# Compute the overall degree of consolidation due to Stage 1 and Stage 2
sum_uini = u1_t1ini + u2_t2ini
sum_ut2fin = u1_t2fin + u2_t2fin
Uvr_t2fin = 1.0 - sum_ut2fin / sum_uini

# Compute the consolidation settlement at the end of construction of Stage 2
S_t2fin = Uvr_t2fin * S_total

# message
print(f'\n15. Consolidation settlement at the end of construction (Stage 2)')
print(f't2fin                        = {t2fin/secs_per_day} days')
print(f'Uv        of stage 1 @ t2fin = {Uv1_t2fin*100:.2f} %')
print(f'Ur        of stage 1 @ t2fin = {Ur1_t2fin*100:.2f} %')
print(f'Uvr       of stage 1 @ t2fin = {Uvr1_t2fin*100:.2f} %')
print(f'Uv        of stage 2 @ t2fin = {Uv2_t2fin*100:.2f} %')
print(f'Ur        of stage 2 @ t2fin = {Ur2_t2fin*100:.2f} %')
print(f'Uvr       of stage 2 @ t2fin = {Uvr2_t2fin*100:.2f} %')
print(f'u1     due to load 1 @ t2ini = {u1_t2fin:.2f} kPa')
print(f'u2     due to load 2 @ t2ini = {u2_t2ini:.2f} kPa')
print(f'u2     due to load 2 @ t2fin = {u2_t2fin:.2f} kPa')
print(f'Uvr of stage 1 and 2 @ t2fin = {Uvr_t2fin*100:.2f} %')
print(f'S   of stage 1 and 2 @ t2fin = {S_t2fin:.2f} m')

# 16. Consolidation settlement at the end of the waiting period (Stage 2) ##########################

# Set time at the end of the wait period of Stage 2 as the final allowed time (1 year)
t2wait = 365 * secs_per_day

# Compute tau at the final time
tau2_t2wait = t2wait - dt2

# Compute the degrees of consolidation due to Stage 1 at the end of wait time of Stage 2
tau1_t2wait = t2wait - dt1
Uv1_t2wait = calc_Uv(tau1_t2wait)
Ur1_t2wait = calc_Ur(tau1_t2wait)
Uvr1_t2wait = calc_Uvr(Uv1_t2wait, Ur1_t2wait)

# Compute the degrees of consolidation due to Stage 2 at the end of wait time of Stage 2
Uv2_t2wait = calc_Uv(tau2_t2wait)
Ur2_t2wait = calc_Ur(tau2_t2wait)
Uvr2_t2wait = calc_Uvr(Uv2_t2wait, Ur2_t2wait)

# Compute the excess pore water pressure due to Stage 1 at the end of wait time of Stage 2
u1_t2wait = u1_t1ini * (1.0 - Uvr1_t2wait)

# Compute the excess pore-water pressure due Stage 2 at the end of wait time of Stage 2
u2_t2wait = u2_t2ini * (1.0 - Uvr2_t2wait)

# Compute the overall degree of consolidation due to Stage 1 and Stage 2
sum_ut2wait = u1_t2wait + u2_t2wait
Uvr_t2wait = 1.0 - sum_ut2wait / sum_uini

# Compute the consolidation settlement at the end of the wait time of Stage 2
S_t2wait = Uvr_t2wait * S_total

print(f'\n16. Consolidation settlement at the end of the waiting period (Stage 2)')
print(f't2wait                        = {t2wait/secs_per_day} days')
print(f'Uv        of stage 1 @ t2wait = {Uv1_t2wait*100:.2f} %')
print(f'Ur        of stage 1 @ t2wait = {Ur1_t2wait*100:.2f} %')
print(f'Uvr       of stage 1 @ t2wait = {Uvr1_t2wait*100:.2f} %')
print(f'Uv        of stage 2 @ t2wait = {Uv2_t2wait*100:.2f} %')
print(f'Ur        of stage 2 @ t2wait = {Ur2_t2wait*100:.2f} %')
print(f'Uvr       of stage 2 @ t2wait = {Uvr2_t2wait*100:.2f} %')
print(f'u1     due to load 1 @ t2wait = {u1_t2wait:.2f} kPa')
print(f'u2     due to load 2 @ t2wait = {u2_t2wait:.2f} kPa')
print(f'Uvr of stage 1 and 2 @ t2wait = {Uvr_t2wait*100:.2f} %')
print(f'S   of stage 1 and 2 @ t2wait = {S_t2wait:.2f} m')

# 17. Post-construction settlement #################################################################

# Compute the remaining settlement
S_rem = S_total - S_t2wait

# Find t corresponding to 99% consolidation (Uvr = 0.99)
def res99(t):
    Uvr_fixed = 0.99
    Uv = calc_Uv(t)
    Ur = calc_Ur(t)
    return Uvr_fixed - 1.0 + (1.0-Uv) * (1.0-Ur)
tverylong = 10000 * secs_per_day
t99 = opt.brentq(res99, 0, tverylong)
t99_days = np.ceil(t99 / secs_per_day)

# Compute the settlement due to traffic loading
dsig_traf = 12.0 # kPa
esigz_traf = esigz_ini + dsigz + dsig_traf
S_traf = H_soil * Cc_soil * np.log10(esigz_traf / esigz_ini) / (1.0 + e0_soil) - S_total

# Compute the secondary settlement
tend_days = 100 * 365.0 # days
S_sec = H_soil * Ca_soil * np.log10(tend_days / t99_days) / (1.0 + e0_soil)

# Compute the post-construction settlement
S_pc = S_rem + S_traf + S_sec

# message
print(f'\n17. Post-construction settlement')
print(f'remaining settlement                 = {S_rem:.2f} m')
print(f'time for 99% consolidation           = {t99_days:.0f} days')
print(f'settlement due to traffic            = {S_traf:.2f} m')
print(f'secondary settlement after 100 years = {S_sec:.2f} m')
print(f'post-construction settlement         = {S_pc:.2f} m')
 
# 18. Plots ########################################################################################

# Plot the fill height versus time
T = np.array([t1ini, t1fin, t1wait, t2fin, t2wait]) / secs_per_day
H = np.array([0.0, H1, H1, H1+H2, H1+H2])
plt.plot(T, H, 'b-o')
plt.xlabel('time [days]')
plt.ylabel('fill height [m]')
plt.grid(linestyle='--',color='grey')
plt.savefig('plot_fill-height-vs-time.png')

# Plot the settlement versus time
S = np.array([ 0.0, S_t1fin, S_t1wait, S_t2fin, S_t2wait])
plt.clf()
plt.plot(T, S, 'r-o')
plt.xlabel('time [days]')
plt.ylabel('settlement [m]')
plt.grid(linestyle='--',color='grey')
plt.gca().invert_yaxis()
plt.savefig('plot_settlement-vs-time.png')

# Plot the excess pore water pressure due to the first embankment
U1 = np.array([u1_t1ini, u1_t1fin, u1_t1wait, u1_t2fin, u1_t2wait])
plt.clf()
plt.plot(T, U1, 'g-o')
plt.xlabel('time [days]')
plt.ylabel('u1 [kPa]')
plt.grid(linestyle='--',color='grey')
plt.savefig('plot_u1-vs-time.png')

# Plot the excess pore water pressure due to the second embankment
U2 = np.array([ 0.0, 0.0, u2_t2ini, u2_t2fin, u2_t2wait])
plt.clf()
plt.plot(T, U2, 'm-o')
plt.xlabel('time [days]')
plt.ylabel('u2 [kPa]')
plt.grid(linestyle='--',color='grey')
plt.savefig('plot_u2-vs-time.png')
