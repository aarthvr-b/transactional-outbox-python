from dataclasses import dataclass

from pydantic import BaseModel, EmailStr, Field


@dataclass(frozen=True)
class CreateOrderCommand:
    customer_email: str
    total_amount: int


class CreateOrderRequest(BaseModel):
    customer_email: EmailStr
    total_amount: int = Field(gt=0)


class CreateOrderResponse(BaseModel):
    order_id: str
    customer_email: str
    total_amount: int
