from app.db import SessionLocal
from app.dispatcher import OutboxDispatcher


def main() -> None:
    with SessionLocal() as session:
        with session.begin():
            dispatcher = OutboxDispatcher(session)
            count = dispatcher.dispatch_once()

        print(f"Dispatched {count} event(s).")


if __name__ == "__main__":
    main()
