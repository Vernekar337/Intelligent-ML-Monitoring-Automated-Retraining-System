from monitoring.pipeline import run_feature_drift_pipeline, run_performance_monitoring
from prediction_drift.pipeline import run_prediction_drift_pipeline
from report.pipeline import run_health_report_pipeline
from retraining.pipeline import run_retraining_pipeline

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

    #Prediction drift
    try:
      prediction_drift_report = run_prediction_drift_pipeline(
          model_version=model_version
      )
    except Exception as e:
      prediction_drift_report = {"error": str(e)}
    system_result["prediction_drift"] = prediction_drift_report

    #Performance drift
    try:
      performance_drift_report = run_performance_monitoring(
          model_version=model_version
      )
    except Exception as e:
      performance_drift_report = {"error": str(e)}
    system_result["performance_drift"] = performance_drift_report

    #Health report
    try:
      health_report = run_health_report_pipeline(
          model_version=model_version
      )
    except Exception as e:
      health_report = {"error": str(e)}
    system_result["health_report"] = health_report

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

    return system_result
