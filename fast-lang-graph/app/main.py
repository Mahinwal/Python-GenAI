from fastapi import FastAPI
from app.config import Config
from app.health_router import router as health_router
from app.chat_router import router as chat_router


# Application configuration
config = Config()

app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description=config.APP_DESCRIPTION
)

app.include_router(health_router)
app.include_router(chat_router)