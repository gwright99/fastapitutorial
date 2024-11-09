import os
from datetime import datetime
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# This loads the Base-derived models we need to create.
import app.models  # noqa: F401
from app.core.config import settings
from app.db.base_class import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Nov 9/2024 - Modify boilerplate to accommodate testing flow
if os.getenv("FASTAPI_TESTING_RUN_ACTIVE", False):
    config.set_main_option("sqlalchemy.url", settings.TEST_DB_URL)
else:
    config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)
    # other values from the config, defined by the needs of env.py, can be acquired:
    # my_important_option = config.get_main_option("my_important_option")

# add your model's MetaData object for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # https://medium.com/alan/making-alembic-migrations-more-team-friendly-e92997f60eb2
    # Customize unique identifier used by Alembic
    def process_revision_directives(context, revision, directives):
        # 20210801211024 for a migration generated on Aug 1st, 2021 at 21:10:24
        rev_id = datetime.now().strftime("%Y%m%d%H%M%S")
        for directive in directives:
            directive.rev_id = rev_id

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,  # <-- new
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
