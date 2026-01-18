import pandas as pd
from retraining.decision import decide_retraining_action, cooldown_decide, fetch_active_model, validate_new_model, update_model_registry, log_retraining_decision
from retraining.data import data_sufficiency_check, build_retraining_dataset, time_based_split
from retraining.training import retrain_model
from ml_db.mongo_client import model_registry_collection


import pandas as pd


def run_retraining_pipeline(actions: dict, model_version : str, health_report_id=None):

    decision = decide_retraining_action(actions)
    active_model = fetch_active_model()

    if decision["decision"] == "no_action":
        log_retraining_decision(decision, active_model, health_report_id=health_report_id)
        return decision

    if not cooldown_decide(active_model["trained_at"]):
        decision = {"decision": "blocked_by_cooldown"}
        log_retraining_decision(decision, active_model, health_report_id=health_report_id)
        return decision

    if not data_sufficiency_check():
        decision = {"decision": "blocked_by_data"}
        log_retraining_decision(decision, active_model, health_report_id=health_report_id)
        return decision

    data = build_retraining_dataset()
    train, _ = time_based_split(data)

    df = pd.DataFrame(train)
    X = df.drop(columns=["churn"])
    y = df["churn"]
    
    PATH = "model/model" + "_" + model_version + ".pkl"

    training_stats = retrain_model(
        X,
        y,
        base_model_path="model/model_v1.pkl",
        preprocessor_path="model/preprocessor.pkl",
        new_model_path= PATH
    )

    if not validate_new_model(
        active_model["metrics"],
        training_stats["metrics"]
    ):
        decision = {
            "decision": "retraining_rejected",
            "reason": "validation_f1_degraded"
        }
        log_retraining_decision(decision, active_model, health_report_id=health_report_id)
        return decision

    update_model_registry(
        old_model=active_model,
        new_model_version="v2",
        training_stats=training_stats,
        samples_used=len(df)
    )

    decision = {"decision": "retrained"}
    log_retraining_decision(
        decision,
        active_model,
        new_model_version="v2",
        health_report_id=health_report_id
    )

    return {
        "decision": "retrained",
        "training_stats": training_stats
    }

