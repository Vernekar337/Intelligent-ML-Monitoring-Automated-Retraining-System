from datetime import datetime, timedelta
from ml_db.mongo_client import model_registry_collection
from ml_db.mongo_client import retraining_decisions_collection


def decide_retraining_action(actions: dict) -> dict:
  
    retraining_recommended = actions.get("retraining_recommended", False)
    urgency = actions.get("urgency", "none")
    reason = actions.get("reason", "")

    if not retraining_recommended:
      decision = "no_action"
    else:
      if urgency == "immediate":
        decision = "retrain_now"
      else:
        decision = "schedule_retrain"

    return {
        "decision": decision,
        "reason": reason,
        "evaluated_at": datetime.utcnow().isoformat()
    }
    
def cooldown_decide(last_trained_at: str, cooldown_days: int = 7) -> bool :
    try:
        last_dt = datetime.fromisoformat(last_trained_at)
    except Exception:
        return True  

    return (datetime.utcnow() - last_dt) >= timedelta(days=cooldown_days)


def validate_new_model(old_metrics: dict, new_metrics: dict) -> bool:
    old_f1 = old_metrics.get("f1")
    new_f1 = new_metrics.get("f1")

    if old_f1 is None or new_f1 is None:
        raise ValueError("F1 metric missing for validation")

    return new_f1 >= old_f1



def fetch_active_model():
    model = model_registry_collection.find_one(
        {"status": "production"},
        sort=[("trained_at", -1)]
    )

    if not model:
        raise RuntimeError("No active production model found in registry")

    return model



def update_model_registry(
    old_model: dict,
    new_model_version: str,
    training_stats: dict,
    samples_used: int
):

    # Mark old model inactive
    model_registry_collection.update_one(
        {"_id": old_model["_id"]},
        {"$set": {"status": "inactive"}}
    )

    # Register new model
    model_registry_collection.insert_one({
        "model_version": new_model_version,
        "parent_version": old_model["model_version"],
        "status": "production",
        "trained_at": datetime.utcnow().isoformat(),
        "training_type": "retraining",
        "samples_used": samples_used,
        "metrics": training_stats["metrics"]
    })
    

def log_retraining_decision(
    decision: dict,
    old_model: dict,
    new_model_version: str = None,
    health_report_id=None
):

    record = {
        "decision": decision["decision"],
        "reason": decision.get("reason"),
        "model_version_before": old_model["model_version"],
        "model_version_after": new_model_version,
        "health_report_id": health_report_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    retraining_decisions_collection.insert_one(record)


