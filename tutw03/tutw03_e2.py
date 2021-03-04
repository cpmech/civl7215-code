import numpy as np
import matplotlib.pyplot as plt

# 1
def consolid_calc_Tv_given_Uv(Uv):
    """Calculates Tv, given Uv, using the approximation formula."""
    if Uv <= 0.526:
        return (np.pi / 4.0) * Uv ** 2
    else:
        return -0.085 - 0.933 * np.log10(1.0 - Uv)


# 2
def consolid_calc_Uv_given_Tv(Tv):
    """Calculate Uv, given Tv, using the approximation formula."""
    if Tv <= 0.217:
        return 2.0 * np.sqrt(Tv / np.pi)
    else:
        a = (1.781 - Tv) / 0.933
        return 1.0 - (10.0 ** a) / 100.0


# 3
def consolid_calc_Uv_given_Tv_series(Tv, nseries=100):
    """Calculate Uv @ time Tv, using the (truncated) Fourier series.
    nseries is the number of terms in the series [optional]"""
    sumx = 0.0
    for m in range(nseries):
        M = (2.0 * m + 1.0) * np.pi / 2.0
        MM = M ** 2.0
        sumx += 2.0 * np.exp(-MM * Tv) / MM
    return 1.0 - sumx


# generate 100 Tv-values from 0 to 1.1 as in Figure 7.8, page 216
Tv_sequence = np.linspace(0, 1.1, 100)

# generate 100 Uv-values from 0 to 0.95 as in Figure 7.8, page 2016
Uv_sequence = np.linspace(0, 0.95, 100)

# because Tv_sequence and Uv_sequence are arrays and the functions
# above contain if-else conditional statements,
# we have to vectorize these functions when passing arrays
# as arguments to them.
calc_Tv_given_Uv = np.vectorize(consolid_calc_Tv_given_Uv)
calc_Uv_given_Tv = np.vectorize(consolid_calc_Uv_given_Tv)
calc_Uv_given_Tv_series = np.vectorize(consolid_calc_Uv_given_Tv_series)

# digitized data from Figure 7.8, page 216
digitized_data = np.array(
    [
        [0.0, 0.19194095],
        [0.0012828202, 5.181788],
        [0.013218241, 11.893543],
        [0.03108148, 19.945795],
        [0.06192362, 27.79931],
        [0.099847235, 35.64912],
        [0.12708025, 40.04955],
        [0.16258639, 45.02148],
        [0.20046441, 50.567997],
        [0.24422847, 55.343662],
        [0.28443658, 59.353413],
        [0.30572277, 61.453644],
        [0.3565607, 65.84172],
        [0.40385032, 69.84776],
        [0.45703733, 73.65878],
        [0.50193983, 76.32248],
        [0.5610205, 79.74652],
        [0.6035473, 81.64369],
        [0.6614287, 84.10865],
        [0.7051282, 85.621315],
        [0.7606339, 87.31975],
        [0.8043296, 88.64047],
        [0.85983527, 90.338905],
        [0.9035233, 91.27575],
        [0.9554731, 92.20827],
        [1.0050625, 93.14202],
        [1.059369, 93.88137],
        [1.1042259, 94.24177],
    ]
)

# 4
plt.plot(
    calc_Tv_given_Uv(Uv_sequence),
    100 * Uv_sequence,
    linestyle="-",
    linewidth=10,
    marker="o",
    markevery=7,
    color="grey",
    label="Tv(Uv)-Uv",
)
plt.plot(
    Tv_sequence,
    100 * calc_Uv_given_Tv(Tv_sequence),
    linestyle="-",
    linewidth=4,
    marker="s",
    markevery=5,
    color="gold",
    label="Tv-Uv(Tv)",
)
plt.plot(
    Tv_sequence,
    100 * calc_Uv_given_Tv_series(Tv_sequence),
    linestyle="-",
    marker="*",
    markevery=3,
    color="black",
    label="Tv-Uv(Tv) series",
)
plt.plot(
    digitized_data[:, 0],
    digitized_data[:, 1],
    linestyle="None",
    marker="*",
    color="red",
    label="digitized data",
)
plt.axis([0, 1.1, 0, 100])
plt.gca().invert_yaxis()
plt.grid(linestyle="--", color="grey")
plt.legend()
plt.xlabel("Time factor Tv")
plt.ylabel("Degree of vertical consolidation Uv (%)")
bbox = {"boxstyle": "round", "facecolor": "white"}
plt.text(0.55, 33, "For the case of uniform\ninitial excess pore pressure", bbox=bbox)
plt.show()
