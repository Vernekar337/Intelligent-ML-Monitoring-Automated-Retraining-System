from monitoring.pipeline import run_feature_drift_pipeline, run_performance_monitoring
from prediction_drift.pipeline import run_prediction_drift_pipeline
from report.pipeline import run_health_report_pipeline
from retraining.pipeline import run_retraining_pipeline
from overall_report import generate_feature_decision, generate_overall_report, generate_retraining_decision, generate_final_report, generate_system_status
from datetime import datetime

def run_system_cycle(model_version: str):

    system_result = {}

    #Feature drift
    try:
      feature_drift_report = run_feature_drift_pipeline(
          model_version=model_version
      )
    except Exception as e:
      feature_drift_report = {"error": str(e)}
    system_result["feature_drift"] = feature_drift_report
    feature_drift_detected = generate_feature_decision(system_result["feature_drift"])

    #Prediction drift
    try:
      prediction_drift_report = run_prediction_drift_pipeline(
          model_version=model_version
      )
    except Exception as e:
      prediction_drift_report = {"error": str(e)}
    system_result["prediction_drift"] = prediction_drift_report
    prediction_drift_detected = generate_overall_report(system_result["prediction_drift"])

    #Performance drift
    try:
      performance_drift_report = run_performance_monitoring(
          model_version=model_version
      )
    except Exception as e:
      performance_drift_report = {"error": str(e)}
    system_result["performance_drift"] = performance_drift_report
    performance_degraded = generate_overall_report(system_result["performance_drift"])

    #Health report
    try:
      health_report = run_health_report_pipeline(
          model_version=model_version
      )
    except Exception as e:
      health_report = {"error": str(e)}
    system_result["health_report"] = health_report
    system_status = generate_system_status(system_result["health_report"])
    
    #Retraining
    try:
      retraining_result = run_retraining_pipeline(
          actions=health_report["actions"],
          health_report_id=health_report["_id"],
          model_version = model_version
      )
    except Exception as e:
      retraining_result = {"error": str(e)}
    system_result["retraining"] = retraining_result
    retraining_triggered = generate_retraining_decision(system_result["retraining"])
    
    final_report = {
      "timestamp" : datetime.utcnow().isoformat(),
      "system_status": system_status,
      "feature_drift_detected": feature_drift_detected,
      "prediction_drift_detected": prediction_drift_detected,
      "performance_degraded": performance_degraded,
      "retraining_triggered": retraining_triggered
    }
    
    generate_final_report(final_report)

    return system_result
