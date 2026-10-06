import json
import aio_pika

from asyncpg import Pool

from app.core.config import settings
from app.core.metrics import shop_orders_created_total
from app.orders import repository
from app.orders.schemas import OrderCreate


async def create_order(pool: Pool,
                       channel: aio_pika.abc.AbstractChannel,
                       data: OrderCreate,) -> dict:

    order = await repository.create_order(pool, data)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps({"order_id": order["id"]}).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=settings.rabbitmq_queue,
    )

    shop_orders_created_total.inc()
    return order


async def get_order(pool: Pool, order_id: int) -> dict | None:
    return await repository.get_order_by_id(pool, order_id)


async def list_orders(pool: Pool) -> list[dict]:
    return await repository.list_orders(pool)
