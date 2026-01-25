import random
from ml_db.mongo_client import prediction_logs_collection, ground_truth_logger_collection
from ground_truth.ground_truth_logger import log_ground_truth


def simulate_ground_truth(
    max_records: int = None,
    churn_probability: float = 0.5
):
    cursor = prediction_logs_collection.find(
        {"actual_churn": {"$exists": False}}
    )

    if max_records:
        cursor = cursor.limit(max_records)

    for pred in cursor:
        prediction_id = pred["_id"]

        actual_churn = 1 if random.random() < churn_probability else 0

        log_ground_truth(prediction_id, actual_churn)

