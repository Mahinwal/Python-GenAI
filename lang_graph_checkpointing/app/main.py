from fastapi import FastAPI

from app.health_route import router as health_router
from app.chat_route import router as chat_router
from app.config import get_settings

settings = get_settings()


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

app.include_router(health_router)
app.include_router(chat_router)
