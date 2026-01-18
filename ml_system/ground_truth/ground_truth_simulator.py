import random
from ml_db.mongo_client import prediction_logs_collection, ground_truth_logger_collection
from ground_truth.ground_truth_logger import log_ground_truth


def simulate_ground_truth(
    max_records: int = None,
    churn_probability: float = 0.5
):
    existing_gt = {
        doc["customer_id"]
        for doc in ground_truth_logger_collection.find()
    }

    cursor = prediction_logs_collection.find()

    if max_records:
        cursor = cursor.limit(max_records)

    for pred in cursor:
        cid = pred["customer_id"]

        if cid in existing_gt:
            continue

        actual_churn = 1 if random.random() < churn_probability else 0
        log_ground_truth(cid, actual_churn)
