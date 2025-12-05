"""Database layer: provides async and sync engines and session helpers.

- Async engine for FastAPI (use AsyncSession via async_session())
- Sync engine helper for Celery and scripts (use sync_session())
"""
import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager, contextmanager

DATABASE_URL_ASYNC = os.getenv('DATABASE_URL_ASYNC', 'postgresql+asyncpg://postgres:postgres@postgres:5432/autoscillab')
DATABASE_URL_SYNC = os.getenv('DATABASE_URL_SYNC', 'postgresql://postgres:postgres@postgres:5432/autoscillab')

# Async engine & sessionmaker for FastAPI
async_engine: AsyncEngine = create_async_engine(DATABASE_URL_ASYNC, echo=False, future=True)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False, future=True)

# Sync engine for Celery tasks and management scripts
sync_engine = create_engine(DATABASE_URL_SYNC, pool_pre_ping=True)

@asynccontextmanager
async def async_session():
    async with async_session_maker() as session:
        yield session

@contextmanager
def sync_session():
    SessionLocal = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def init_db():
    # create tables (sync) for migrations-less demo; recommend Alembic in prod
    SQLModel.metadata.create_all(bind=sync_engine)
