import sys
import os

from datetime import datetime
from typing import List, Dict, Any
from ml_db.mongo_client import prediction_drift_report_collection
from monitoring.psi import calculate_psi_drift, classify_probability_psi


def build_prediction_drift_report(
    model_version: str,
    window_type: str,                 
    window_size: int,                 
    reference_probability_distribution: List[float],
    current_probability_distribution: List[float],
    probability_psi: float,
    class_balance_delta: float
) -> Dict[str, Any]:

    class_balance_delta = class_balance_delta
    drift_status = classify_probability_psi(probability_psi)

    report = {
        "drift_type": "prediction_drift",
        "model_version": model_version,

        "window": {
            "type": window_type,
            "size": window_size
        },

        "metrics": {
            "probability_psi": round(probability_psi, 4),
            "class_balance_delta": round(class_balance_delta, 4)
        },

        "distributions": {
            "reference_probability_distribution": reference_probability_distribution,
            "current_probability_distribution": current_probability_distribution
        },

        "status": drift_status,
        "generated_at": datetime.utcnow().isoformat()
    }
    prediction_drift_report_collection.insert_one(report)

    return report