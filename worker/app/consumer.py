import asyncio
import json
import aio_pika
import structlog

from asyncpg import Pool

from app.config import settings
from app.processor import process_order

log = structlog.get_logger()


async def _consume_once(pool: Pool) -> None:
    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(settings.rabbitmq_queue, durable=True)
    log.info("Worker started, listen queue '%s'", settings.rabbitmq_queue)

    try:
        async with queue.iterator(timeout=None) as it:
            async for message in it:
                async with message.process():
                    data = json.loads(message.body.decode())
                    order_id = data.get("order_id")
                    request_id = data.get("request_id", "unknown")

                    if order_id is None:
                        log.error("No field 'order_id': %s", data)
                        continue

                    structlog.contextvars.clear_contextvars()
                    structlog.contextvars.bind_contextvars(
                        request_id=request_id, service="worker"
                    )

                    log.info("message_received", order_id=order_id,
                             queue=settings.rabbitmq_queue)

                    await process_order(pool, order_id,
                                        settings.processing_delay_ms)

    finally:
        await connection.close()


async def consume(pool: Pool) -> None:
    while True:
        try:
            await _consume_once(pool)
        except Exception:
            log.exception("Consumer crashed, restarting in 5 seconds")
            await asyncio.sleep(5)
