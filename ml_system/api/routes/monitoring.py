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

@router.get("/system/health")

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

@router.get("/feature-drift")

def get_latest_feature_drift_report():
  report = feature_drift_reports_collection.find_one(
    sort =[("generated_at", -1)]
  )
  
  if not report:
    raise HTTPException(
      status_code= 404,
      detail= 'No health report found'
    )
    
  features = []
  for i in report['feature_metrics']:
      features.append({
          "name" : i,
          "status" : report['feature_metrics'][i]['status']
        })

  return {
    "model_version" : report['model_version'],
    "window_type" : report['window']['type'],
    "window_size" : report['window']['size'],
    "features" : features
    
  }
  
@router.get("/prediction-drift")

def get_latest_prediction_drift_report():
  report = prediction_drift_report_collection.find_one(
      sort = [("generated_at", -1)]
   )
  
  if not report:
    raise HTTPException(
      status_code= 404,
      detail= 'No prediction drift report found'
    )

  return {
    "model_version" : report['model_version'],
    "psi" : report["metrics"]['probability_psi'],
    "status" : report['status'],
    "distribution" : {
      "train" : [i for i in report['distributions']['reference_probability_distribution']],
      "current" : [i for i in report['distributions']['current_probability_distribution']]
    }
  }
  


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


                          
@router.get("/performance")

def get_latest_performance_report():
  report = performance_drift_reports_collection.find_one(
    sort =[("generated_at", -1)]
  )
  
  if not report:
        raise HTTPException(
            status_code=404,
            detail="No performance report found"
        )
  
  history = performance_drift_reports_collection.find(
    sort =[("generated_at", -1)]
  )
  
  if not history:
        raise HTTPException(
            status_code=404,
            detail="No historty found"
        )
  accuracy_list = []
  history_list = list(history)
  for i in history_list: 
    accuracy_list.append({
      'timestamp' : i['generated_at'],
      'accuracy' : i['metrics']['accuracy']
    })
    
  return {
        "model_version": report["model_version"],
        "metrics": report["metrics"],
        "generated_at": report["generated_at"],
        "history" : accuracy_list
    }
  
  
  
  

@router.get("/ping")

def monitoring_ping():
  return {"message" : "Monitoring router working"}

