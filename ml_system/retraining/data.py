
import pandas as pd
from sklearn.model_selection import train_test_split
from ml_db.mongo_client import prediction_logs_collection
from retraining.training import full_data_generator

def data_sufficiency_check(min_samples: int = 1000) -> bool:
    count = prediction_logs_collection.count_documents(
        {"actual_label": {"$exists": True}}
    )
    return count >= min_samples
      

FEATURE_COLUMNS = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "Contract",
    "PaymentMethod",
    "InternetService",
    "num_support_tickets"
]


def build_retraining_dataset(limit: int = None) -> list:
    cursor = prediction_logs_collection.find(
        {"actual_label": {"$exists": True}},
        sort=[("timestamp", -1)]
    )

    if limit:
        cursor = cursor.limit(limit)

    rows = []
    for doc in cursor:
        row = {k: doc["features"][k] for k in FEATURE_COLUMNS}
        row["churn"] = doc["actual_label"]
        rows.append(row)

    return rows
      
def time_based_split(data: list, train_ratio: float = 0.8):
  split_idx = int(len(data) * train_ratio)
  train = data[:split_idx]
  val = data[split_idx:]
  return train, val

  
  
def final_split(full_data_X, full_Data_y):
    X_train, X_val, y_train, y_val = train_test_split(full_data_X, full_Data_y, train_size=0.8, random_state=42)
    return X_train, X_val, y_train, y_val
      