from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.db import Base, make_url_sync
import app.models as models
import app.config as config

context_config = context.config

if context_config.config_file_name is not None:
    fileConfig(context_config.config_file_name)

target_metadata = Base.metadata

context_config.set_main_option("sqlalchemy.url", make_url_sync(config.POSTGRES_DSN))


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        context_config.get_section(context_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
