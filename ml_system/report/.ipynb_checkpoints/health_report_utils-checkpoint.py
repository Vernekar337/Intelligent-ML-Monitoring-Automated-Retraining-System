def overall_status(per_status, predict_status, feature_status):
  if (per_status == "major_drift"):
    overall_status = "critical"

  elif (predict_status == "major_drift"):
    overall_status = "warning"

  elif(feature_status == "major_drift"):
    overall_status = "warning"

  else:
    overall_status = "healthy"
    
  return overall_status


def actions_data(performance_drift, prediction_drift, feature_drift):
  actions = {}
  
  if(performance_drift == "major_drift"):
    actions = {
      "retraining_recommended": True,
      "urgency": "immediate",
      "reason": "major_performance_drift_detected"
    }
    
  elif(performance_drift == "no_drift" and prediction_drift == "major_drift"):
    actions = {
      "retraining_recommended": False,
      "urgency": "monitor",
      "reason": "prediction_drift_detected_without_performance_degradation"
    }
    
  elif(performance_drift == "no_drift" and prediction_drift == "no_drift" and feature_drift == "major_drift"):
    actions = {
      "retraining_recommended": False,
      "urgency": "observe",
      "reason": "feature_drift_detected_upstream_only"
    }
  
  else:
    actions = {
      "retraining_recommended": False,
      "urgency": "none",
      "reason": "model_operating_within_expected_ranges"
    }
    
  return actions