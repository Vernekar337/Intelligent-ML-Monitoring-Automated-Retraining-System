from datetime import datetime
from ml_db.mongo_client import (
    feature_drift_reports_collection,
    performance_drift_reports_collection,
    prediction_drift_report_collection,
    model_health_reports_collection,
)
from report.health_report_utils import overall_status, actions_data


def run_health_report_pipeline(model_version: str) -> dict:
    feature_drift = list(
        feature_drift_reports_collection.find().sort("timestamp", -1).limit(1)
    )
    performance_drift = list(
        performance_drift_reports_collection.find().sort("timestamp", -1).limit(1)
    )
    prediction_drift = list(
        prediction_drift_report_collection.find().sort("timestamp", -1).limit(1)
    )

    if not (feature_drift and performance_drift and prediction_drift):
        raise RuntimeError("Missing drift reports to generate health report")

    feature_status = feature_drift[0]["summary"]["overall_status"]
    prediction_status = prediction_drift[0]["status"]
    performance_status = performance_drift[0]["status"]

    report = {
        "model_version": model_version,
        "health_snapshot": {
            "feature_drift": feature_status,
            "prediction_drift": prediction_status,
            "performance_drift": performance_status,
        },
        "overall_status": overall_status(
            performance_status,
            prediction_status,
            feature_status,
        ),
        "actions": actions_data(
            performance_status,
            prediction_status,
            feature_status,
        ),
        "source_reports": {
            "feature_drift_report_id": feature_drift[0]["_id"],
            "prediction_drift_report_id": prediction_drift[0]["_id"],
            "performance_drift_report_id": performance_drift[0]["_id"],
        },
        "generated_at": datetime.utcnow().isoformat(),
    }

    model_health_reports_collection.insert_one(report)
    return report
