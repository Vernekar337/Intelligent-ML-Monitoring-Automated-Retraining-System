
from sklearn.metrics import confusion_matrix


# evaluation/metrics.py

def compute_confusion_matrix(joined_records):

    TP = TN = FP = FN = 0

    for record in joined_records:
        pred = record["prediction"]
        actual = record["actual_label"]

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
    
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    return {
        "confusion_matrix": cm,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "total_samples": total
    }




