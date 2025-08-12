from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .settings import settings

engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS runs(
          id TEXT PRIMARY KEY, goal TEXT, state TEXT, created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS steps(
          run_id TEXT, step_id TEXT, kind TEXT, state TEXT, deps TEXT, PRIMARY KEY(run_id, step_id)
        );
        CREATE TABLE IF NOT EXISTS events(
          run_id TEXT,
          seq BIGSERIAL PRIMARY KEY,
          ts TIMESTAMP DEFAULT NOW(),
          level TEXT,
          event TEXT,
          payload JSONB
        );
        CREATE TABLE IF NOT EXISTS artifacts(
          run_id TEXT, path TEXT, sha256 TEXT, size BIGINT, PRIMARY KEY(run_id, path)
        );
        """))
