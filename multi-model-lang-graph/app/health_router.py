from fastapi import APIRouter

router = APIRouter(prefix="", tags=["health"])

@router.get("/health")
async def health_root() -> dict[str, str]:
    return {"status": "up"}

