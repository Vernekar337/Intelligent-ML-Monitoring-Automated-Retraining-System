from fastapi import APIRouter,  HTTPException
from api.utils.mongo import serialize_object
from ml_db.mongo_client import (
  prediction_drift_report_collection,
  performance_drift_reports_collection,
  feature_drift_reports_collection,
  model_health_reports_collection
)

router = APIRouter(
  prefix ="/monitoring",
  tags=["Monitoring"]
)

@router.get("/health/latest")

def get_latest_health_report():
  report = model_health_reports_collection.find_one(
    sort =[("generated_at", -1)]
  )
  
  if not report:
    raise HTTPException(
      status_code= 404,
      detail= 'No health report found'
    )
  
  return serialize_object(report)

@router.get("/drift/{drift_type}")

def get_latest_drift_report(drift_type: str):
  if drift_type == 'feature':
    collection = feature_drift_reports_collection
    
  elif drift_type == 'performance':
    collection = performance_drift_reports_collection
    
  elif drift_type == "prediction":
    collection = prediction_drift_report_collection
  
  else:
    raise HTTPException(
      status_code= 404,
      detail = "No collection found"
    )
    
  report = collection.find_one(
    sort = [("generated_at", -1)]
  )
  
  if not report:
    raise HTTPException(
      status_code= 404,
      detail = f"No {drift_type} drift reports found"
    )
  return serialize_object(report)
                          


@router.get("/ping")

def monitoring_ping():
  return {"message" : "Monitoring router working"}