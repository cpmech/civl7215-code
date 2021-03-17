import numpy as numpy

# 0 Input data

tamper_weight_tf = 18.2 # ton
tamper_diameter_m = 1.5 # m
tamper_height_m = 1.5 # m

# 1 depth of improvement and nc ##########################################

# selected depth of improvement
Di = 8.2

# shallow leachate (high saturation) and semipervious with silts
nc = 0.35

# message
print('\n1 Depth of improvement and nc')
print('---------------------------------------------')
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
print('---------------------------------------------')
print(f'Energy per blow = {Ed_tfm:.0f} tf-m')
print(f'Energy per blow = {Ed:.0f} kJ')
print(f'Drop height     = {Hd:.1f} m')
