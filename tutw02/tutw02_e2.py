import numpy as np
import matplotlib.pyplot as plt

# table data
eff_stresses = np.array([10.0, 20.0, 40.0, 80.0, 160.0, 320.0])
void_ratios = np.array([0.910, 0.851, 0.760, 0.629, 0.490, 0.352])

# given data
z = 2.5  # [m] => depth of soil sample
gn = 19.0  # [kN/m³] => natural/saturated unit weight
k = 6.5e-7  # [m/s] => permeability
sigp = 33.0  # [kPa] => effective preconsolidation stress

# some constants
gw = 9.81  # [kN/m³] => unit weight of water

# 1
sigz0 = z * (gn - gw)

# 2
OCR = sigp / sigz0

# 3
sig0 = eff_stresses[0]
sig1 = eff_stresses[1]
e0 = void_ratios[0]
e1 = void_ratios[1]
Cr = (e0 - e1) / np.log10(sig1 / sig0)

# 4
siga = eff_stresses[3]
sigb = eff_stresses[5]
ea = void_ratios[3]
eb = void_ratios[5]
Cc = (ea - eb) / np.log10(sigb / siga)

# 5 (interpolate void ratios first)
sigm = 100.0
sign = 200.0
em = (void_ratios[3] + void_ratios[4]) / 2.0
en = (void_ratios[4] + void_ratios[5]) / 2.0
av = (em - en) / (sign - sigm)

# 6
mv = av / (1.0 + e0)

# 7
cv = k / (gw * mv)

# print results
print(f"1. eff overb stress,   sigz0 = {sigz0:.2f}")
print(f"2. overconsolid ratio, OCR   = {OCR:.2f}")
print(f"3. coef of recomp,     Cr    = {Cr:.2f}")
print(f"4. coef of comp,       Cc    = {Cc:.2f}")
print(f"5. coef of comp.lty    av    = {av:.6f}")
print(f"6. coef of vol comp,   mv    = {mv:.6f}")
print(f"7. coef of consolid,   cv    = {cv:.2e}")

# plot table data
plt.plot(eff_stresses, void_ratios)
plt.xscale("log")
plt.xlabel("stress [kPa]")
plt.ylabel("void ratio")
plt.grid()
plt.show()
