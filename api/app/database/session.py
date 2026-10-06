import asyncpg

from app.core.config import settings

_pool: asyncpg.Pool | None = None


async def init_pool() -> asyncpg.Pool:
    global _pool
    _pool = await asyncpg.create_pool(
        user=settings.postgres_user,
        password=settings.postgres_password,
        database=settings.postgres_db,
        host=settings.postgres_host,
        port=settings.postgres_port,
        min_size=1,
        max_size=16,
    )
    return _pool


async def close_pool() -> None:
    if _pool is not None:
        await _pool.close()


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Pool not created, check config.py")
    return _pool
