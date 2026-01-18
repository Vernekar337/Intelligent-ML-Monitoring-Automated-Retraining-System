
import datetime
from ml_db.mongo_client import ground_truth_logger_collection 

def log_ground_truth( customer_id, actual_churn ):
  record = {
    "customer_id" : customer_id,
    "actual_churn" : actual_churn,
    "observed_at" : datetime.utcnow().isoformat()
  }
  ground_truth_logger_collection.insert_one(record)