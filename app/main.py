from fastapi import FastAPI

from app.api import router
from app.db import Base, engine
from app import models


app = FastAPI(title="Transactional Outbox Demo")


@app.on_event("startup")
def on_startuo() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


app.include_router(router)
