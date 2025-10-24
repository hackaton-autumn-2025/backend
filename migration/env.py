from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

from src.infrastructure.base import Base

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.configs import settings


config = context.config
section = config.config_ini_section
config.set_section_option(
    section, 'sqlalchemy.url', settings.db_settings.sync_database_url
)


def run_migrations_offline():
    context.configure(
        url=settings.sync_database_url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        {'sqlalchemy.url': settings.db_settings.sync_database_url},
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
