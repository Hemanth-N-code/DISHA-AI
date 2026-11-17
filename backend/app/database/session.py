# backend/app/database/session.py
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings

logger = logging.getLogger(__name__)

db_url = settings.DATABASE_URL
connect_args = {}

if db_url.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False,
        "timeout": 15
    }
    # NullPool prevents holding open SQLite connection handles across requests
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        poolclass=NullPool
    )
    
    # Configure SQLite pragmas for maximum concurrency
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA busy_timeout=5000")
            cursor.close()
        except Exception:
            pass
else:
    try:
        # Test connecting to Postgres
        temp_engine = create_engine(db_url, pool_pre_ping=True)
        with temp_engine.connect() as conn:
            pass
        engine = temp_engine
        logger.info("Successfully connected to PostgreSQL database.")
    except Exception as e:
        logger.warning(f"Failed to connect to PostgreSQL at {db_url}: {e}. Falling back to SQLite.")
        sqlite_url = "sqlite:///./disha.db"
        engine = create_engine(
            sqlite_url,
            connect_args={"check_same_thread": False, "timeout": 15},
            poolclass=NullPool
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            db.rollback()
        except Exception:
            pass
        db.close()
