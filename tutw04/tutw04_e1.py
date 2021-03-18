import numpy as numpy

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
Hd = Ed_tfm / tamper_weight_tf # m

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

# assuming that the crater depth is 1.5
d_cd = 1.5 # m

# compute the required applied energy for ironing passes
# using again the first part of Equation 3.21,
# but with UAE_total replaced by UAE_IP and Di replaced by crater depth
AE_IP = UAE_IP * d_cd # kJ/m2

# message
print(f'\n4 Applied energy during the ironing pass (IP)')
print(f'Average UAE during ironing = {UAE_IP} kJ/m³')
print(f'Crater depth               = {d_cd} m')
print(f'AE ironing                 = {AE_IP:.0f} kJ/m²')

# 5 Applied energy during the high-energy pass (HEP) #####################

# multiple passes are recommended to disspate the pore pressure.
# assuming 2 passes
N_p = 2

# compute the applied energy during HEP
AE_HEP = (AE_total - AE_IP) / N_p

# message
print(f'\nApplied energy during the high-energy pass (HEP)')
print(f'Number of passes = {N_p}')
print(f'AE high-energy   = {AE_HEP:.0f} kJ/m²')
