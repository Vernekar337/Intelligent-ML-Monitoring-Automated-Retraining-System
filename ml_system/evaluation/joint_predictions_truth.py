from typing import List, Dict   
from ml_db.mongo_client import prediction_logs_collection, ground_truth_logger_collection, performance_drift_reports_collection
from datetime import datetime


def get_joined_prediction_records(
    model_version: str,
    window_size: int = 100
) -> List[Dict]:

    cursor = (
        prediction_logs_collection
        .find({
            "model_version": model_version,
            "actual_churn": {"$exists": True}
        })
        .sort("timestamp", -1)
        .limit(window_size)
    )

    records = list(cursor)

    if not records:
        return []

    joined_records = []

    for r in records:
        joined_records.append({
            "customer_id": r.get("customer_id"),
            "prediction": int(r["prediction"]),
            "actual_label": int(r["actual_churn"]),
            "predicted_at": r["timestamp"],
            "model_version": r["model_version"]
        })
        

    return joined_records

def save_performance_drift_report(
    model_version: str,
    metrics: dict,
    status: str
):
    record = {
        "model_version": model_version,
        "metrics": metrics,
        "status": status,
        "generated_at": datetime.utcnow()
    }

    performance_drift_reports_collection.insert_one(record)


