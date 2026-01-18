def normalize_distribution_for_psi(feature_distribution: dict) -> dict:
    normalized = {}

    for bin_name, values in feature_distribution.items():
        normalized[bin_name] = {
            "reference": values["reference%"] / 100,
            "current": values["current%"] / 100
        }

    return normalized
