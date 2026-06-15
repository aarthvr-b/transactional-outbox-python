from app.db import SessionLocal
from app.schemas import CreateOrderCommand
from app.services import OrderService


def main() -> None:
    command = CreateOrderCommand(
        customer_email="arthur@example.com",
        total_amount=4999,
    )

    with SessionLocal() as session:
        with session.begin():
            service = OrderService(session)
            order = service.create_order(command)

        print(f"Created order: {order.id}")

    if __name__ == "__main__":
        main()
