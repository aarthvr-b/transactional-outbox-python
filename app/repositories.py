import json
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Order, OutboxEvent, OutboxStatus, utc_now


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order) -> None:
        self.session.add(order)


class OutboxRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_event(
        self,
        *,
        event_type: str,
        aggregate_type: str,
        aggregate_id: str,
        payload: dict,
    ) -> OutboxEvent:
        event = OutboxEvent(
            event_type=event_type,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            payload=json.dumps(payload),
            status=OutboxStatus.PENDING.value,
        )

        self.session.add(event)
        return event

    def get_pending_events(self, limit: int = 10) -> list[OutboxEvent]:
        statement = (
            select(OutboxEvent)
            .where(OutboxEvent.status == OutboxStatus.PENDING.value)
            .order_by(OutboxEvent.created_at)
            .limit(limit)
        )

        return list(self.session.scalars(statement).all())

    def mark_as_published(self, event: OutboxEvent) -> None:
        event.status = OutboxStatus.PUBLISHED.value
        event.published_at = utc_now()

    def mark_as_failed(self, event: OutboxEvent, error: Exception) -> None:
        event.retry_count += 1
        event.last_error = str(error)
