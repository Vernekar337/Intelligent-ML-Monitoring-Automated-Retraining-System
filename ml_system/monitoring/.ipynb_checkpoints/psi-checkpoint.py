
import numpy as np

EPSILON = 1e-4 

def calculate_psi(distribution: dict) -> float:

    psi_total = 0.0

    for bin_name, values in distribution.items():
        r = values.get("reference", 0)
        c = values.get("current", 0)

        if r == 0:
            r = EPSILON
        if c == 0:
            c = EPSILON

        psi_contribution = (c - r) * np.log(c / r)
        psi_total += psi_contribution

    return psi_total

def classify_psi(psi_value):
    if psi_value > 0.2:
        status = "drift_detected"
    elif psi_value > 0.1:
        status = "watch"
    else:
        status = "no_drift"
    return status
    