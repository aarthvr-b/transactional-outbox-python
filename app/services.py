from sqlalchemy.orm import Session


from app.models import Order
from app.repositories import OrderRepository, OutboxRepository
from app.schemas import CreateOrderCommand


class OrderService:
    def __init__(self, session: Session):
        self.session = session
        self.orders = OrderRepository(session)
        self.outbox = OutboxRepository(session)

    def create_order(self, command: CreateOrderCommand) -> Order:
        order = Order(
            customer_email=command.customer_email, total_amount=command.total_amount
        )

        self.orders.add(order)

        self.outbox.add_event(
            event_type="OrderCreated",
            aggregate_type="Order",
            aggregate_id=order.id,
            payload={
                "order_id": order.id,
                "customer_email": order.customer_email,
                "total_amount": order.total_amount,
            },
        )

        return order
