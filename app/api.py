from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.db import SessionLocal
from app.schemas import CreateOrderCommand, CreateOrderRequest, CreateOrderResponse
from app.services import OrderService

router = APIRouter()


def get_db_session():
    with SessionLocal() as session:
        yield session


@router.post("/orders", response_model=CreateOrderResponse)
def create_order(
    request: CreateOrderRequest,
    session: Session = Depends(get_db_session),
) -> CreateOrderResponse:
    with session.begin():
        service = OrderService(session)
        order = service.create_order(
            CreateOrderCommand(
                customer_email=request.customer_email,
                total_amount=request.total_amount,
            )
        )

    return CreateOrderResponse(
        order_id=order.id,
        customer_email=order.customer_email,
        total_amount=order.total_amount,
    )
