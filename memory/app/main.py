
from fastapi import FastAPI

from app.config import get_settings
from app.health_route import router as health_router
from app.chat_route import router as chat_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description    
)

app.include_router(health_router)
app.include_router(chat_router)