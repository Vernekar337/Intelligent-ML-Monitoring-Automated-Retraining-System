
from datetime import datetime
from ml_db.mongo_client import prediction_logs_collection


def log_prediction(model_version, features, prediction, prediction_percentage):
    record = {
        "customer_id": features['customer_id'],
        "timestamp": datetime.utcnow().isoformat(),
        "model_version": model_version,
        "features": features,
        "prediction": prediction,
        "prediction_percentage": prediction_percentage
    }

    prediction_logs_collection.insert_one(record)

