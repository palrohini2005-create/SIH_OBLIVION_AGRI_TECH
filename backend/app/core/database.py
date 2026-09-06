"""SQLAlchemy engine, session factory and the FastAPI dependency.

SQLite specifics worth knowing:

- ``check_same_thread=False`` is required because FastAPI serves requests from a
  thread pool, and SQLite otherwise refuses a connection used from more than one
  thread.
- WAL journalling lets a reader and a writer work at the same time, which is
  what you want as soon as two requests overlap.
- Foreign keys are off by default in SQLite and have to be switched on per
  connection, which is what the event listener below does.
"""

from collections.abc import Generator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Parent of every ORM model in app/models.py."""


@event.listens_for(Engine, "connect")
def _configure_sqlite(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_db() -> Generator[Session, None, None]:
    """Request-scoped session.

    Use it as a dependency::

        @router.get("/things")
        def things(db: Session = Depends(get_db)):
            ...

    The session is closed when the request finishes, whatever happened.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
