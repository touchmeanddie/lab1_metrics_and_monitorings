from fastapi import APIRouter, Depends, HTTPException, Request
from asyncpg import Pool

from app.database.session import get_pool
from app.orders import service
from app.orders.schemas import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


def get_rabbit_channel(request: Request):
    return request.app.state.rabbit_channel


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    data: OrderCreate,
    pool: Pool = Depends(get_pool),
    channel=Depends(get_rabbit_channel),
):
    return await service.create_order(pool, channel, data)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, pool: Pool = Depends(get_pool)):
    order = await service.get_order(pool, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Not Found")
    return order


@router.get("", response_model=list[OrderResponse])
async def list_orders(pool: Pool = Depends(get_pool)):
    return await service.list_orders(pool)
