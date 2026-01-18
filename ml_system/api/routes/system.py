from fastapi import APIRouter, HTTPException
from orchestrator import run_system_cycle
from api.utils.mongo import serialize_object

router = APIRouter(
  prefix= "/system",
  tags=["System"]
)


@router.post("/run")
def run_system(model_version : str):
  try:
    result = run_system_cycle(model_version)
    return serialize_object(result)
    
  except Exception as e:
    raise HTTPException(
      status_code= 500,
      detail = f"System run failed: {str(e)}"
    )
    
    
@router.get("/ping")

def system_ping():
  return {"message" : "System router working"}