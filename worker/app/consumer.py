import json
import logging
import aio_pika

from asyncpg import Pool

from app.config import settings
from app.processor import process_order

logger = logging.getLogger(__name__)


async def consume(pool: Pool) -> None:
    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(settings.rabbitmq_queue, durable=True)
    logger.info(
        "Worker started, listen queue '%s'",
        settings.rabbitmq_queue)

    async with queue.iterator(timeout=None) as it:
        async for message in it:
            async with message.process():
                data = json.loads(message.body.decode())
                order_id = data.get("order_id")

                if order_id is None:
                    logger.error("No field 'order_id': %s", data)
                    continue

                await process_order(pool, order_id,
                                    settings.processing_delay_ms)
