from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrderCommand:
    customer_email: str
    total_amount: int
