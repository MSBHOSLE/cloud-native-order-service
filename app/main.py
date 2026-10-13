from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.orders import router as orders_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Cloud-Native Order Processing Microservice with state machine lifecycle, idempotency controls, and metrics.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router, prefix="/api/v1")


@app.get("/health/live", tags=["Kubernetes Probes"])
async def liveness_probe():
    return {"status": "alive"}


@app.get("/health/ready", tags=["Kubernetes Probes"])
async def readiness_probe():
    return {"status": "ready"}
