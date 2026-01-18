def normalize_distribution_for_psi(feature_distribution: dict) -> dict:
    normalized = {}

    for bin_name, values in feature_distribution.items():
        normalized[bin_name] = {
            "reference": values["reference%"] / 100,
            "current": values["current%"] / 100
        }

    return normalized


def max_psi(feature_drift : dict):
    max = 0;
    for i, j in feature_drift.items():
        if(j['psi'] > max):
            max = j['psi']
            
    return max;
        
def num_features_drifted(feature_drift : dict):
    count = 0;
    for i, j in feature_drift.items():
        if(j['status'] in ['drift_detected', 'watch']):
            count += 1
            
    return count;

def num_features_major_drift(feature_drift : dict):
    count = 0;
    for i, j in feature_drift.items():
        if(j['status'] == 'drift_detected'):
            count += 1
            
    return count;

def overall_status(statuses):

    if not statuses:
        return "no_data"

    if isinstance(statuses, dict):
        values = statuses.values()
    else:
        values = statuses

    if "drift_detected" in values:
        return "drift_detected"

    if "watch" in values:
        return "watch"

    return "no_drift"

        
