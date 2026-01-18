import sys
import os
import random

PROJECT_ROOT = r"C:\Users\Sahil.s.Vernekar\OneDrive\Documents\ML\Churn\ml_system"
sys.path.insert(0, PROJECT_ROOT)

print("Project root added:", PROJECT_ROOT)

from ground_truth.ground_truth_logger import log_ground_truth
from ml_db.mongo_client import prediction_logs_collection
from ml_db.mongo_client import ground_truth_logger_collection

preds_customer = prediction_logs_collection.find()
gt_customers = {t["customer_id"]: t for t in ground_truth_logger_collection.find()}
Ids =[]

def log_simulate(preds_customer, gt_customers): 
    for p in preds_customer:
        cid = p["customer_id"]
        if cid in gt_customers:
            continue;
        else:
            actual_churn = random.choice([0, 1])
            log_ground_truth( cid, actual_churn )
    
log_simulate(preds_customer, gt_customers)