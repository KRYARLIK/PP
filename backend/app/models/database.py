import time
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db(max_attempts: int = 30, delay_seconds: float = 2.0) -> None:
    """Create database tables, retrying while PostgreSQL starts."""
    # Import models so SQLAlchemy knows their metadata.
    from app.models import document, search_history  # noqa: F401

    last_error: Exception | None = None
    for _ in range(max_attempts):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception as exc:  # pragma: no cover - exercised in Docker startup
            last_error = exc
            time.sleep(delay_seconds)
    raise RuntimeError("Database did not become ready") from last_error


def get_db() -> Generator[Session, None, None]:
    """Provide a database session to a request and always close it."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
