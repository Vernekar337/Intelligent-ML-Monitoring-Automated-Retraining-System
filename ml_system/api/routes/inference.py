from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from inference.predict import predict
from fastapi import HTTPException

class InferenceRequest(BaseModel):
    features: Dict[str, Any]

class InferenceResponse(BaseModel):
  prediction: int
  probability: float | None = None
  model_version: str
  
  
router = APIRouter(
  prefix= "/inference",
  tags = ["Inference"]
)

@router.post("/predict", response_model=InferenceResponse)

def predict_endpoint(request : InferenceRequest):
  try:
    pred, proba, model = predict(
      input_features= request.features,
      model_version= 'v1',
      model_path= 'model/model_v1.pkl',
      preprocessor_path= 'model/preprocessor.pkl'
    )

    return InferenceResponse(
      prediction=int(pred),
      probability= proba,   
      model_version=model
    )
  except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {str(e)}"
        )
  
def inference_ping():
  return {"message": "Inference router working"}


