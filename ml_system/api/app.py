from fastapi import FastAPI
from api.routes.monitoring import router as monitoring_router
from api.routes.inference import router as inference_router
from api.routes.system import router as system_router
from api.routes.retraining import router as retraining_router
from api.routes.registry import router as registry_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
  title="ML Monitoring & Retraining System",
  description="API layer over the ML system",
  version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inference_router)
app.include_router(monitoring_router)
app.include_router(system_router)
app.include_router(retraining_router)
app.include_router(registry_router)

@app.get("/")

def health_check():
  return {"status" : "API is running"}
