from evaluation.metrics import compute_metrics
from monitoring.performance_utility import drift_decision
from monitoring.drift_utils import overall_status
from evaluation.joint_predictions_truth import get_joined_prediction_records, save_performance_drift_report
from datetime import datetime
import numpy as np
import json
from typing import Dict

from ml_db.mongo_client import (
    prediction_logs_collection,
    feature_drift_reports_collection
)

from monitoring.drift_utils import overall_status



def run_performance_monitoring(model_version: str) -> dict:
    joined_records = get_joined_prediction_records(model_version)
    metrics = compute_metrics(joined_records)

    drift_status = drift_decision(
        acc_drop=1 - metrics["accuracy"],
        f1_drop=1 - metrics["f1"]
    )
    save_performance_drift_report(
        model_version=model_version,
        metrics=metrics,
        status=drift_status
    )


    return {
        "metrics": metrics,
        "status": drift_status
    }


FEATURE_COLUMNS = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "num_support_tickets",
    "Contract",
    "InternetService",
]

MEAN_SHIFT_THRESHOLD = 2.0
STD_RATIO_THRESHOLD = 1.5
CATEGORICAL_SHIFT_THRESHOLD = 0.3
CATEGORICAL_WARN_THRESHOLD = 0.15

print("DEBUG: entered feature drift")


def run_feature_drift_pipeline(
    model_version: str,
    window_size: int = 100
) -> Dict:

    records = list(
        prediction_logs_collection
        .find({"model_version": model_version})
        .sort("timestamp", -1)
        .limit(window_size)
    )

    if not records:
        report = {
            "drift_type": "feature_drift",
            "model_version": model_version,
            "summary": {"overall_status": "no_data"},
        }
        feature_drift_reports_collection.insert_one(report)
        return report

    feature_data = {f: [] for f in FEATURE_COLUMNS}

    for r in records:
        features = r.get("features", {})
        for f in FEATURE_COLUMNS:
            if f in features:
                feature_data[f].append(features[f])

    path = f"experiments/training_stats_{model_version}.json"
    try:
        with open(path, "r") as f:
            baseline_stats = json.load(f)
    except FileNotFoundError:
        report = {
            "drift_type": "feature_drift",
            "model_version": model_version,
            "summary": {"overall_status": "no_data"},
        }
        feature_drift_reports_collection.insert_one(report)
        return report

    feature_metrics = {}

    for feature, values in feature_data.items():

        baseline = baseline_stats.get(feature)

        if baseline is None:
            continue

        if not values:
            continue

        if not isinstance(baseline, dict):
            continue

        # NUMERICAL FEATURE
        if "mean" in baseline and "std" in baseline:
            curr_mean = float(np.mean(values))
            curr_std = float(np.std(values))

            base_mean = baseline["mean"]
            base_std = baseline["std"] if baseline["std"] > 0 else 1e-6

            mean_shift = abs(curr_mean - base_mean) / base_std
            std_ratio = curr_std / base_std

            if mean_shift > MEAN_SHIFT_THRESHOLD or std_ratio > STD_RATIO_THRESHOLD:
                status = "drift_detected"
            elif mean_shift > MEAN_SHIFT_THRESHOLD / 2:
                status = "watch"
            else:
                status = "no_drift"

            feature_metrics[feature] = {
                "type": "numerical",
                "mean_shift": round(mean_shift, 3),
                "std_ratio": round(std_ratio, 3),
                "status": status,
            }

        # CATEGORICAL FEATURE
        else:
            values = [str(v) for v in values]
            total = len(values)

            curr_dist = {
                k: v / total
                for k, v in zip(*np.unique(values, return_counts=True))
            }

            shift = sum(
                abs(baseline.get(k, 0) - curr_dist.get(k, 0))
                for k in baseline.keys()
            )

            if shift > CATEGORICAL_SHIFT_THRESHOLD:
                status = "drift_detected"
            elif shift > CATEGORICAL_WARN_THRESHOLD:
                status = "watch"
            else:
                status = "no_drift"

            feature_metrics[feature] = {
                "type": "categorical",
                "distribution_shift": round(shift, 3),
                "status": status,
            }

    if not feature_metrics:
        report = {
            "drift_type": "feature_drift",
            "model_version": model_version,
            "summary": {"overall_status": "no_data"},
        }
        feature_drift_reports_collection.insert_one(report)
        return report

    statuses = [m["status"] for m in feature_metrics.values()]

    overall = overall_status(statuses)

    report = {
        "drift_type": "feature_drift",
        "model_version": model_version,
        "window": {
            "type": "count_based",
            "size": window_size,
        },
        "feature_metrics": feature_metrics,
        "summary": {
            "num_features_drifted": sum(
                1 for s in statuses if s in ("drift_detected", "watch")
            ),
            "overall_status": overall,
        },
        "generated_at": datetime.utcnow().isoformat(),
    }

    feature_drift_reports_collection.insert_one(report)
    return report



