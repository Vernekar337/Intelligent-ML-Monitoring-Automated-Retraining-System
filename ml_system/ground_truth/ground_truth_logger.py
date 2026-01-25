from datetime import datetime
from ml_db.mongo_client import prediction_logs_collection

def log_ground_truth(prediction_id, actual_churn):
    prediction_logs_collection.update_one(
        {"_id": prediction_id},
        {
            "$set": {
                "actual_churn": actual_churn,
                "observed_at": datetime.utcnow().isoformat()
            }
        }
    )
