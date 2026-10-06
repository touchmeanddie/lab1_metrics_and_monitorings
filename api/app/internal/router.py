from fastapi import APIRouter, Depends
from asyncpg import Pool
from app.database.session import get_pool
from app.orders import repository

router = APIRouter(prefix="/internal", tags=["internal"])


@router.get("/stats")
async def stats(pool: Pool = Depends(get_pool)):
    raw = await repository.get_stats(pool)
    last = raw["last_processed_at"]
    return {
        "orders_new": raw["orders_new"],
        "orders_processing": raw["orders_processing"],
        "orders_done": raw["orders_done"],
        "last_processed_at": last.isoformat() if last else None,
    }
