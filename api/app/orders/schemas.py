from datetime import datetime
from pydantic import BaseModel, PositiveFloat, PositiveInt


class OrderCreate(BaseModel):
    amount: PositiveFloat
    items_count: PositiveInt


class OrderResponse(BaseModel):
    id: int
    amount: float
    items_count: int
    status: str
    created_at: datetime
    processed_at: datetime | None = None
