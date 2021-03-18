import numpy as np

# 0 Input data

tamper_weight_tf = 18.2 # ton
tamper_diameter_m = 1.5 # m
tamper_height_m = 1.5 # m

# 1 Depth of improvement and nc ##########################################

# selected depth of improvement
Di = 8.2

# shallow leachate (high saturation) and semipervious with silts
nc = 0.35

# message
print('\n1 Depth of improvement and nc')
print(f'Depth of improvement = {Di} m')
print(f'Coefficient nc       = {nc}')

# 2 Energy per blow and drop height ######################################

# required energy per blow (ton-meter)
Ed_tfm = (Di / nc) ** 2.0 # tf-m

# convert energy to kJ
Ed = Ed_tfm * 9.81 # kJ

# drop height
# round up the result
Hd = np.ceil( Ed_tfm / tamper_weight_tf ) # m

# message
print('\n2 Energy per blow and drop height')
print(f'Energy per blow = {Ed_tfm:.0f} tf-m')
print(f'Energy per blow = {Ed:.0f} kJ')
print(f'Drop height     = {Hd:.1f} m')

# 3 Required total applied energy ########################################

# for landfills, the UAE ranges from 600 to 1100 kJ/m3; taking an average
UAE_ave =(600 + 1100) / 2.0 # kJ/m3

# total applied energy using the first part of Equation 3.21
AE_total = UAE_ave * Di # kJ/m2

# message
print('\n3 Required total applied energy')
print(f'Average UAE = {UAE_ave} kJ/m³')
print(f'AE total    = {AE_total:.0f} kJ/m²')

# 4 Applied energy during the ironing pass (IP) ##########################

# assuming that the geomaterial above the landfill is fine grained
# UAE for semipervious fine-grained soils (average)
UAE_IP = (250 + 350) / 2.0 # kJ/m3

# assuming that the crater depth for the IP is 1.5
d_cd_ip = 1.5 # m

# compute the required applied energy for ironing passes
# using again the first part of Equation 3.21,
# but with UAE_total replaced by UAE_IP and Di replaced by crater depth
AE_IP = UAE_IP * d_cd_ip # kJ/m2

# message
print('\n4 Applied energy during the ironing pass (IP)')
print(f'Average UAE during ironing = {UAE_IP} kJ/m³')
print(f'Crater depth               = {d_cd_ip} m')
print(f'AE ironing                 = {AE_IP:.0f} kJ/m²')

# 5 Applied energy during the high-energy pass (HEP) #####################

# multiple passes are recommended to disspate the pore pressure.
# assuming 2 passes
Np = 2

# compute the applied energy during HEP
AE_HEP = (AE_total - AE_IP) / Np

# message
print('\n5 Applied energy during the high-energy pass (HEP)')
print(f'Number of passes = {Np}')
print(f'AE high-energy   = {AE_HEP:.0f} kJ/m²')

# 6 Pattern, spacing and number of drops #################################

# typical drop spacing is 1.5 to 2.5 times the tamper diameter
# adopted drop spacing factor
drop_spacing_factor = 2.0

# compute the drop spacing
s = drop_spacing_factor * tamper_diameter_m

# compute the equivalent influence area
Ae = s ** 2.0

# compute the number of drops at each specific drop point
# (round up and convert to integer)
W_kN = tamper_weight_tf * 9.81
Nd = int(np.ceil( AE_HEP * Ae / (W_kN * Hd) ))

# message
print('\n6 Pattern, spacing and number of drops')
print(f'drop spacing for a square pattern  = {s} m')
print(f'equivalment influence area         = {Ae} m²')
print(f'Number of drops at each drop point = {Nd}')

# 7 Allowed crater depth #################################################

# estimate the crater depth
d_cd_estim = 0.028 * (Nd ** 0.55) * np.sqrt(tamper_weight_tf * Hd)

# allowed crater depth
d_cd_allowed = tamper_height_m + 0.3

# message
print('\n7 Allowed crater depth')
print(f'crater depth estimate = {d_cd_estim:.2f} m')
print(f'allowed crater depth  = {d_cd_allowed:.2f} m')
print(f'satisfactory          = {d_cd_estim <= d_cd_allowed}')

# 8 Induced settlement estimate (method 1) ###############################

# considering the landfill as an uncontrolled fill,
# the induced settlement factor ranges from 5% to 20%
# taking the average for the induced settlement factor
settle_factor_ave = (5 + 20) / 2.0

# estimate the possible induced settlement
S_1 = Di * settle_factor_ave / 100.0

# message
print('\n8 Induced settlement estimate (method 1)')
print(f'average settlement factor    = {settle_factor_ave:.2f} %')
print(f'possible settlement estimate = {S_1:.2f} m')

# 9 Induced settlement estimate (method 2) ###############################

# compute the area of each crater,
# assuming the crater diameter to be the same as the tamper diameter
A_crater = np.pi * (tamper_diameter_m / 2.0) ** 2.0

# compute the area ratio of improvement
a_s = A_crater / Ae

# estimate the settlement
S_2 = Np * a_s * d_cd_estim

print('\n9 Induced settlement estimate (method 2)')
print(f'crater area                  = {A_crater:.2f} m²')
print(f'area ration of improvement   = {a_s:.2f}')
print(f'possible settlement estimate = {S_2:.2f} m')
