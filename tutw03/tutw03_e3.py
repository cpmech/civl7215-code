import numpy as np


def consolid_calc_Tv_given_Uv(Uv):
    """Calculates Tv, given Uv, using the approximation formula."""
    if Uv <= 0.526:
        return (np.pi / 4.0) * Uv ** 2
    else:
        return -0.085 - 0.933 * np.log10(1.0 - Uv)


# input data
H = 8.0  # [m]
hdr = H  # [m] (singly-drained)
cv = 2e-7  # [m²/s]

# some constants
seconds_per_day = 24.0 * 60.0 * 60.0
seconds_per_year = seconds_per_day * 365.0

# 1
Tv50 = consolid_calc_Tv_given_Uv(0.5)
t50 = Tv50 * (hdr ** 2.0) / cv
t50y = t50 / seconds_per_year
print(f"time to reach 50 % settlement = {t50y:.1f} years")

# 2
Tv90 = consolid_calc_Tv_given_Uv(0.9)
t90 = Tv90 * (hdr ** 2.0) / cv
t90y = t90 / seconds_per_year
print(f"time to reach 90 % settlement = {t90y:.1f} years")
