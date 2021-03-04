import numpy as np
import matplotlib.pyplot as plt

fb = np.zeros((10))
fb[0] = 0.0
fb[1] = 1.0
for i in range(2, 10):
    fb[i] = fb[i - 1] + fb[i - 2]

print("\nthe whole sequence is:")
print(fb)

print("\nstarting from the second, up to the last-but-one:")
print(fb[1:-1])

print("\nstarting from the third number:")
print(fb[2:])

ratios = fb[2:] / fb[1:-1]
print("\nthe ratios are:")
print(ratios)

golden_ratio = (1.0 + np.sqrt(5.0)) / 2.0

plt.plot(ratios)
plt.axhline(golden_ratio, color="gold")
plt.show()
