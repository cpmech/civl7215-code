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

print(f'\n3. Embankment (fill) data')
print(f'H     = {H_fill} m')
print(f'gamma = {gamma_fill} kN/m³')
print(f'c     = {c_fill} kPa')
print(f'phi   = {phi_fill} °')

# 4. Pre-fabricated drains (PVD) ###################################################################

# Width (b) and thickness (tg)
# Spacing and discharge capacity (Qc)
# Compute the equivalent diameter of drain (dc)
# Compute the equivalent influence diameter (de)
# Compute the diameter ratio (Nd)

# 5. Geotechnical problem ##########################################################################

# Factor of safety for bearing capacity
# Drainage length (hdr)
# Depth of middle of the clay layer
# Assume construction rate (e.g. 0.3 m / week)
# Compute auxiliary coefficients bv and br
# Compute the Fm(Nd) coefficient for the radial flow equation

# 6. Functions #####################################################################################

# Define functions to calculate Uv, Ur, and Uvr
# Define a function to calculate the residual from Uvr and the fixed 80% value

# 7. Maximum fill height ###########################################################################

# Compute the allowed pressure based on the foundation undrained strength
# Compute the maximum allowed height of fill
# Round down maximum fill height
 
# 8. Total primary settlement ######################################################################

# Compute the total stress increment
# Compute the initial and final effective stresses at the mid-depth of the soft soil
# Compute the total primary settlement
 
# 9. Data for the first loading stage ##############################################################

# Choose height of the fill for the first loading stage
# Compute the time period for the construction of the first stage
# Round-up the number of days
# Compute the time at the beginning and at the end of construction, and the shift-time for Stage 1

# 10. Consolidation settlement at the end of construction (Stage 1) ################################

# Compute the degrees of consolidation due to Stage 1 at the end of construction of Stage 1
# Compute the excess pore water pressure due to Stage 1 at the end of construction of Stage 1
# Compute the consolidation settlement at the end of construction of Stage 1

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
