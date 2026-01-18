import sys
import os
import random
import datetime

PROJECT_ROOT = r"C:\Users\Sahil.s.Vernekar\OneDrive\Documents\ML\Churn\ml_system"
sys.path.insert(0, PROJECT_ROOT)

print("Project root added:", PROJECT_ROOT)
from evaluation.joint_predictions_truth import joint_prediction
from sklearn.metrics import confusion_matrix

joined_records = joint_prediction()
# evaluation/metrics.py

def compute_confusion_matrix(joined_records):
    """
    joined_records: list of dicts
    Each dict must have:
        - "prediction": 0 or 1
        - "actual": 0 or 1
    """

    TP = TN = FP = FN = 0

    for record in joined_records:
        pred = record["prediction"]
        actual = record["actual"]

        if pred == 1 and actual == 1:
            TP += 1
        elif pred == 0 and actual == 0:
            TN += 1
        elif pred == 1 and actual == 0:
            FP += 1
        elif pred == 0 and actual == 1:
            FN += 1

    return {
        "TP": TP,
        "TN": TN,
        "FP": FP,
        "FN": FN
    }


def compute_metrics(joined_records):
    """
    Computes post-deployment metrics from joined prediction–ground truth data.
    """

    if not joined_records:
        return {
            "error": "No joined records available for evaluation"
        }

    cm = compute_confusion_matrix(joined_records)

    TP = cm["TP"]
    TN = cm["TN"]
    FP = cm["FP"]
    FN = cm["FN"]

    total = TP + TN + FP + FN

    accuracy = (TP + TN) / total if total > 0 else None
    precision = TP / (TP + FP) if (TP + FP) > 0 else None
    recall = TP / (TP + FN) if (TP + FN) > 0 else None

    return {
        "confusion_matrix": cm,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "total_samples": total
    }




