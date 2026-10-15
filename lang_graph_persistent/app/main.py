from contextlib import asynccontextmanager
from fastapi import FastAPI
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

from app.health_route import router as health_router
from app.chat_route import router as chat_router
from app.config import get_settings
from app.graph import build_graph

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    with ConnectionPool(
        conninfo=settings.DATABASE_URL.get_secret_value(),
        max_size=20,
        kwargs={"autocommit": True, "prepare_threshold": 0}

    ) as pool:
        checkpointer = PostgresSaver(pool)
        checkpointer.setup() # creates checkpoint tables if they don't exist — safe to call every startup

        app.state.graph = build_graph(checkpointer)
        
        yield

app = FastAPI(
    title=settings.APP_NAME, 
    version=settings.APP_VERSION, 
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(chat_router)
