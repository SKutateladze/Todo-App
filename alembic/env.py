import asyncio
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from app.dependencies import Base  # your models' Base

DATABASE_URL = "sqlite+aiosqlite:///./todoapp.db"
target_metadata = Base.metadata

def run_migrations_offline():
    """Offline migrations."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Online migrations using async engine."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())  # <-- run the async migration properly
