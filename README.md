# Transactional Outbox Demo

Small Python demo of transactional outbox pattern using FastAPI, SQLAlchemy, and SQLite.

When order gets created, app stores:
- order record in `orders`
- outbox event in `outbox_events`

Both writes happen in same database transaction. Separate dispatcher later reads pending outbox events and "publishes" them with fake publisher.

## Requirements

- Python 3.10+
- `pip`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py
```

Default database file: `outbox_demo.db`

## Run API

```bash
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Create order:

```bash
curl -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_email":"arthur@example.com","total_amount":4999}'
```

Response shape:

```json
{
  "order_id": "uuid",
  "customer_email": "arthur@example.com",
  "total_amount": 4999
}
```

## Run Dispatcher

Dispatch pending outbox events:

```bash
python scripts/run_dispatcher.py
```

Dispatcher prints published event payload and marks event as published in database.

## Demo Scripts

You can also use helper scripts directly:

```bash
python scripts/create_order.py
python scripts/run_dispatcher.py
```

`create_order.py` inserts sample order and matching outbox event without going through HTTP API.
