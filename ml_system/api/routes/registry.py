from fastapi import APIRouter

router = APIRouter(
  prefix = "/registry",
  tags=["Registry"]
)

@router.get("/ping")

def retraining_ping():
  return {"message" : "Registry router working"}