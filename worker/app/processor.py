import asyncio
import time
from datetime import datetime, timezone

from asyncpg import Pool

from app.metrics import shop_order_processing_duration_seconds


async def process_order(pool: Pool, order_id: int, delay_ms: int) -> None:
    start = time.monotonic()

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

    shop_order_processing_duration_seconds.observe(time.monotonic() - start)
