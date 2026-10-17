import asyncio
import asyncpg
import structlog

from prometheus_client import start_http_server

from app.config import settings
from app.consumer import consume
from app.logging_config import setup_logging

structlog.contextvars.bind_contextvars(service="worker")
setup_logging()


async def main() -> None:
    start_http_server(settings.worker_metrics_port)

    pool = await asyncpg.create_pool(
        user=settings.postgres_user,
        password=settings.postgres_password,
        database=settings.postgres_db,
        host=settings.postgres_host,
        port=settings.postgres_port,
        min_size=1,
        max_size=10,
    )

    try:
        await consume(pool)
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
