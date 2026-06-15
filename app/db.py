from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///outbox_demo.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=False)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
