run_system_pipeline(model_version: str) -> dict
feature_drift
prediction_drift
performance_drift
health_report
retraining_decision

predict(input_features: dict) -> float
logs prediction
stores timestamp
stores model_version

run_retraining_pipeline(actions: dict) -> dict
retrained / skipped
reason
model_version (new or same)

Read-only contracts (future APIs)
get_latest_health_report()
get_drift_history(drift_type)
get_model_registry()
