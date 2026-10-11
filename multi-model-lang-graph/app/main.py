from fastapi import FastAPI
from app.health_router import router as health_router
from app.service_router import router as service_router

app = FastAPI(title="LangGraph multi-model minimal application")

app.include_router(health_router)
app.include_router(service_router)