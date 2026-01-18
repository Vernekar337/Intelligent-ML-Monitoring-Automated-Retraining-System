import sys
import os
import random
import datetime

PROJECT_ROOT = r"C:\Users\Sahil.s.Vernekar\OneDrive\Documents\ML\Churn\ml_system"
sys.path.insert(0, PROJECT_ROOT)

print("Project root added:", PROJECT_ROOT)

from ml_db.mongo_client import prediction_logs_collection
from ml_db.mongo_client import ground_truth_logger_collection

def joint_prediction(): 
    preds_customer = prediction_logs_collection.find()
    gt_customers = {t["customer_id"]: t for t in ground_truth_logger_collection.find()}
    results = []
    for p in preds_customer:
        cid = p["customer_id"]
        if cid in gt_customers:
            results.append({
                "customer_id" : cid,
                "prediction" : p["prediction"],
                "actual" : gt_customers[cid]["actual_churn"],
                "timestamp" : p["timestamp"],
                "model_version" : p["model_version"]
                })
    return results;
    