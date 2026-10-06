from datetime import datetime, timezone
from asyncpg import Pool

from app.orders.schemas import OrderCreate


async def create_order(pool: Pool, data: OrderCreate) -> dict:
    row = await pool.fetchrow(
        """
        INSERT INTO orders (amount, items_count, status, created_at)
        VALUES ($1, $2, 'NEW', $3)
        RETURNING *
        """,
        float(data.amount), data.items_count, datetime.now(timezone.utc),
    )
    return dict(row)


async def get_order_by_id(pool: Pool, order_id: int) -> dict | None:
    row = await pool.fetchrow(
        "SELECT * FROM orders WHERE id = $1", order_id
        )
    return dict(row) if row else None


async def list_orders(pool: Pool) -> list[dict]:
    rows = await pool.fetch(
        "SELECT * FROM orders ORDER BY id DESC LIMIT 15"
        )
    return [dict(r) for r in rows]


async def get_stats(pool: Pool) -> dict:
    row = await pool.fetchrow(
        """SELECT
            count(CASE WHEN status = 'NEW' THEN 1 END)
            AS orders_new,
            count(CASE WHEN status = 'PROCESSING' THEN 1 END)
            AS orders_processing,
            count(CASE WHEN status = 'DONE' THEN 1 END)
            AS orders_done,
            max(CASE WHEN status = 'DONE' THEN processed_at END)
            AS last_processed_at
        FROM orders"""
        )
    return dict(row)
