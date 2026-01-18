
def compute_metrics(TP, TN, FP, FN, N) -> dict:
    accuracy = (TP + TN) / N

    if(TP + FP == 0):
        precision = TP / (0.00001)
    else:
        precision = TP/ (TP + FP)

    if(TP + FN == 0):
        recall = TP / (0.00001)
    else:
        recall = TP / (TP + FN)
        
    f1 = 2*((precision * recall) / (precision + recall))

    report = {
            'accuracy' : accuracy,
            'precision' : precision,
            'recall' : recall,
            'f1' : f1
        }
    return report
  
def compute_confusion_matrix(logs : list) -> dict:
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    N = len(logs)

    for i in range(len(logs)):
        if logs[i]['prediction'] == 1.0 and logs[i]['actual_label'] == 1 :
            TP += 1
        elif logs[i]['prediction'] == 1.0 and logs[i]['actual_label'] == 0 :
            FP += 1
        elif logs[i]['prediction'] == 0.0 and logs[i]['actual_label'] == 0 :
            TN += 1
        elif logs[i]['prediction'] == 0.0 and logs[i]['actual_label'] == 1:
            FN += 1
        else:
            raise ValueError("Invalid prediction/label combination")

    
    report = compute_metrics(TP, TN, FP, FN, N)
    return report
     
def drift_decision(acc_drop, f1_drop):
    if f1_drop > 0.15 or acc_drop > 0.10:
        return "major_drift"

    elif f1_drop > 0.05 or acc_drop > 0.05:
        return "moderate_drift"

    else:
        return "no_drift"
     