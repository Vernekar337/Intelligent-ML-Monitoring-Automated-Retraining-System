from typing import List, Dict   
from ml_db.mongo_client import prediction_logs_collection, ground_truth_logger_collection


def get_joined_prediction_records(
    model_version: str,
    window_size: int = 100
) -> List[Dict]:

    prediction_cursor = (
        prediction_logs_collection
        .find({"model_version": model_version})
        .sort("timestamp", -1)
        .limit(window_size)
    )

    predictions = list(prediction_cursor)

    if not predictions:
        return []

    ground_truth_cursor = ground_truth_logger_collection.find()
    ground_truth = list(ground_truth_cursor)

    gt_lookup = {}
    for gt in ground_truth:
        cid = gt["customer_id"]
        observed_at = gt.get("observed_at")

        if cid not in gt_lookup:
            gt_lookup[cid] = gt
        else:
            if observed_at > gt_lookup[cid].get("observed_at"):
                gt_lookup[cid] = gt

    joined_records = []

    for p in predictions:
        cid = p.get("customer_id")

        if cid not in gt_lookup:
            continue

        joined_records.append({
            "customer_id": cid,
            "prediction": int(p["prediction"]),
            "actual_label": int(gt_lookup[cid]["actual_churn"]),
            "predicted_at": p["timestamp"],
            "model_version": p["model_version"]
        })

    return joined_records
