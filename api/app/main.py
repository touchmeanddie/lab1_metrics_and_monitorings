import aio_pika

from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from fastapi.responses import PlainTextResponse

from app.core.config import settings
from app.core.middleware import MetricsMiddleware
from app.database.database import ORDERS_DDL
from app.database.session import init_pool, close_pool
from app.orders.router import router as orders_router
from app.internal.router import router as internal_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await init_pool()
    async with pool.acquire() as conn:
        await conn.execute(ORDERS_DDL)

    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )
    channel = await connection.channel()
    await channel.declare_queue(settings.rabbitmq_queue, durable=True)

    app.state.rabbit_connection = connection
    app.state.rabbit_channel = channel

    yield

    await connection.close()
    await close_pool()

app = FastAPI(title="Заказики", lifespan=lifespan)
app.add_middleware(MetricsMiddleware)

app.include_router(orders_router)
app.include_router(internal_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics", include_in_schema=False)
async def metrics():
    return PlainTextResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
