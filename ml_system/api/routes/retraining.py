from fastapi import APIRouter, HTTPException
from retraining.pipeline import run_retraining_pipeline
from api.utils.mongo import serialize_object
from pydantic import BaseModel
from typing import Optional, Dict, Any

class RetrainingRequest(BaseModel):
  actions : Dict[str, Any]
  model_version: str
  health_report_id : Optional[str] = None
  

router = APIRouter(
  prefix = "/retraining",
  tags=["Retraining"]
)

@router.post("/run")

def run_Retraining(request: RetrainingRequest):
  try:
    result = run_retraining_pipeline(
      actions= request.actions,
      model_version= request.model_version,
      health_report_id= request.health_report_id
    )
    return serialize_object(result)
    
  except Exception as e:
    raise HTTPException(
      status_code= 500,
      detail= f"Retraining run failed: {str(e)}"
    )
    

@router.get("/ping")

def retraining_ping():
  return {"message" : "Retraining router working"}