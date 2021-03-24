'''
KNOWN
  * fine content about 8% (no clay)
  * min-max void ratios of 0.456-0.950
  * initial void ratio of 0.673
  * design requires Dr > 75%
  * Large HP vibrator (HP100) is available
REQUIRED
  * spacing in triangular pattern
  * subsidence without backfill
'''

# 0 Input data ###########################################################

h = 5.0 # m
e_min = 0.456
e_max = 0.950
e0 = 0.673
Dr = 75.0 / 100.0

# 1 Spacing ##############################################################

# using Figure 3.41 to read the influence coefficient IC_total
IC_total = 12.5
IC = IC_total / 3.0

# using Figure 3.41 again with IC to read the distance from the vibroflot
s = 1.7 # m

# message
print(f'Influence coefficient IC = {IC:.2f}')
print(f'Spacing                s = {s} m')

# 2 Subsidence ###########################################################

# final void ratio
e1 = e_max - Dr * (e_max - e_min)

# average ground subsidence
S = h * (e0 - e1) / (1.0 + e0)

# message
print(f'Final void ratio         e1 = {e1:.3f}')
print(f'Average ground subsidence S = {S:.3f} m')
