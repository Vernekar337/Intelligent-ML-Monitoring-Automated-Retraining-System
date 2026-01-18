from datetime import datetime, timedelta
from typing import Dict
import sys
import os
import numpy as np

PROJECT_ROOT = r"C:\Users\Sahil.s.Vernekar\OneDrive\Documents\ML\Churn\ml_system"
sys.path.insert(0, PROJECT_ROOT)

print("Project root added:", PROJECT_ROOT)

from ml_db.mongo_client import model_registry_collection
from ml_db.mongo_client import temp_prediction_log_collection


def decide_retraining_action(actions: Dict) -> Dict:
  
    retraining_recommended = actions.get("retraining_recommended", False)
    urgency = actions.get("urgency", "none")
    reason = actions.get("reason", "")

    decision = "no_action"

    if retraining_recommended:
        if urgency == "immediate":
            decision = "retrain_now"
        else:
            decision = "schedule_retrain"

    return {
        "decision": decision,
        "reason": reason,
        "evaluated_at": datetime.utcnow().isoformat()
    }

def model_parcer(actions: Dict):
    model_registry_collection.insert_one(actions)
    

def cooldown_decide(ip_date: str) -> bool :
    dt = datetime.fromisoformat(ip_date)
    diff = datetime.now() - dt
    if(diff >= timedelta(days= 7)):
        return True
    else:
        return False
    
def data_sufficiency_check() -> bool:
    N = 1000
    pred_cursor = temp_prediction_log_collection.find({
    "actual_label": {"$exists": True}
    })
    preds = list(pred_cursor)
    retraining_number = len(preds)
    print(retraining_number)
    if(retraining_number >= N):
        return True
    else:
        return False
    
def retraining_dataset() -> dict:
    pred_cursor = temp_prediction_log_collection.find({
    "actual_label": {"$exists": True}
    }).sort('timestamp', -1)
    preds = list(pred_cursor)
    # print(preds)
    features = ['customer_id']+[i for i in preds[0]['features']]
    retraining_rows = []
    
    for p in preds:
            retraining_rows.append({
                "customer_id": p['customer_id'],
                "tenure": p['features']['tenure'],
                "MonthlyCharges": p['features']['MonthlyCharges'],
                "TotalCharges": p['features']['TotalCharges'],
                "Contract": p['features']['Contract'],
                "PaymentMethod": p['features']['PaymentMethod'],
                "InternetService": p['features']['InternetService'],
                "num_support_tickets": p['features']['num_support_tickets'],
                "churn" : p['actual_label']
            })
    train_validation_split(retraining_dataset, preds)            
    return retraining_rows

def train_validation_split(data: dict, preds:list) -> dict:
    split_index = int(0.8 * len(preds))
    data_list = list(data)
    train_data = data_list[:split_index]
    val_data = data_list[split_index:]
    print(train_data)
    print(val_data)
    
   
# "customer_id": "C410",
#           "tenure": 90,
#           "MonthlyCharges": 42.0,
#           "TotalCharges": 3780.0,
#           "Contract": "Two year",
#           "PaymentMethod": "Bank transfer",
#           "InternetService": "DSL",
#           "num_support_tickets": 0

# {'_id': ObjectId('694fac434ff3c44f85fa4e16'), 'customer_id': 'C400', 'timestamp': '2025-12-27T09:52:03.621222', 'model_version': 'v1', 'features': {'tenure': 10, 'MonthlyCharges': 70.5, 'TotalCharges': 85.0, 'Contract': 'Month-to-month', 'PaymentMethod': 'Electronic check', 'InternetService': 'Fiber optic', 'num_support_tickets': 21}, 'prediction': 1.0, 'prediction_percentage': [0.6696590185165405], 'actual_label': 1}