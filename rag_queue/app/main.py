import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Path
from typing import Annotated
from dotenv import load_dotenv

from app.ingest import run_ingestion
from app.worker import run_query
from app.queue_config import queue

load_dotenv()  # Load environment variables from .env file
logger = logging.getLogger("uvicorn.error")


async def run_ingestion_background():
    """Runs the blocking ingestion function in a separate thread
    so it doesn't block the event loop or app startup."""
    try:
        await asyncio.to_thread(run_ingestion)
    except Exception:
        logger.exception("Background ingestion failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_ingestion_background())
    app.state.ingestion_task = task

    yield

    if not task.done():
        logger.info("Waiting for ingestion task to finish before shutdown...")
        await task

app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ingestion-status")
async def ingestion_status():
    task = app.state.ingestion_task

    if task.done():
        if task.exception():
            return {"status": "failed", "error": str(task.exception())}
        return {"status": "complete"}
    return {"status": "running"}


@app.post("/chat")
async def chat(
    query: Annotated[str, Query(..., description="Enter prompt")]
):
    job = queue.enqueue(run_query, query)
    return {"status": "queued", "job_id": job.id}


@app.get("/result/{job_id}")
async def get_result(
    job_id: Annotated[str, Path(..., description="Enter job_id")]
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    return {"result": result}

