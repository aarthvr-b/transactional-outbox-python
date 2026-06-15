import json
from sqlalchemy.orm import Session

from app.repositories import OutboxRepository


class FakePublisher:
    def publish(self, event_type: str, payload: dict) -> None:
        print(f"Publishing event: {event_type}")
        print(payload)


class OutboxDispatcher:
    def __init__(self, session: Session):
        self.session = session
        self.outbox = OutboxRepository(session)
        self.publisher = FakePublisher()

    def dispatch_once(self, limit: int = 10) -> int:
        events = self.outbox.get_pending_events(limit=limit)

        for event in events:
            try:
                payload = json.loads(event.payload)

                self.publisher.publish(
                    event_type=event.event_type,
                    payload=payload,
                )

                self.outbox.mark_as_published(event)
            except Exception as error:
                self.outbox.mark_as_failed(event, error)

        return len(events)
