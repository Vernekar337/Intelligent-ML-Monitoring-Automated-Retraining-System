import sys
import os

PROJECT_ROOT = r"C:\Users\Sahil.s.Vernekar\OneDrive\Documents\ML\Churn\ml_system"
sys.path.insert(0, PROJECT_ROOT)

print("Project root added:", PROJECT_ROOT)

import json
import datetime
import random

from datetime import datetime
from ml_db.mongo_client import ground_truth_logger_collection 

def log_ground_truth( customer_id ):
  actual_churn = random.choice([0, 1])
  record = {
    "customer_id" : customer_id,
    "actual_churn" : actual_churn,
    "observed_at" : datetime.utcnow()
  }
  ground_truth_logger_collection.insert_one(record)