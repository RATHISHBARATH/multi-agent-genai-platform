"""Alembic env.py template for SQLModel + asyncpg

Before using, ensure alembic.ini has sqlalchemy.url set to sync DB URL or set env var.
"""
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
from api.models.models import *
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

config = context.config
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def run_migrations_offline():
    url = os.getenv('DATABASE_URL_SYNC', 'postgresql://postgres:postgres@postgres:5432/autoscillab')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_async_engine(os.getenv('DATABASE_URL_ASYNC', 'postgresql+asyncpg://postgres:postgres@postgres:5432/autoscillab'))
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, process_revision_directives=None)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
