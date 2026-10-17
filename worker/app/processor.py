import asyncio
import time
import structlog
from datetime import datetime, timezone

from asyncpg import Pool

from app.metrics import shop_order_processing_duration_seconds

log = structlog.get_logger()


async def process_order(pool: Pool, order_id: int, delay_ms: int) -> None:
    start = time.monotonic()

    log.info("processing_started", order_id=order_id)

    async with pool.acquire() as connection:
        await connection.execute(
            "UPDATE orders SET status = 'PROCESSING' WHERE order_id = $1",
            order_id,
        )
        await asyncio.sleep(delay_ms / 1000.0)
        await connection.execute(
            """UPDATE orders SET status = 'DONE',
            processed_at = $1
            WHERE order_id = $2""",
            datetime.now(timezone.utc), order_id,
        )

    duration_ms = (time.monotonic() - start) * 1000
    log.info("processing_finished", order_id=order_id,
             duration_ms=round(duration_ms, 2))

    shop_order_processing_duration_seconds.observe(time.monotonic() - start)
