from logging.config import fileConfig

import alembic_postgresql_enum  # noqa: F401
from alembic import context
from sqlalchemy import engine_from_config, pool

from backend.env import get_db_config
from backend.src.database import BaseAlchemyModel

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
from backend.src.authors.models import AuthorsModel  # noqa: F401
from backend.src.books.models import BooksModel  # noqa: F401
from backend.src.books_authors.models import BooksAuthorsModel  # noqa: F401
from backend.src.books_tags.models import BooksTagsModel  # noqa: F401
from backend.src.chapters.models import ChaptersModel  # noqa: F401
from backend.src.tags.models import TagsModel  # noqa: F401
from backend.src.users.models import UsersModel  # noqa: F401
from backend.src.users_books.models import UsersBooksModel  # noqa: F401
from backend.src.volumes.models import VolumesModel  # noqa: F401

target_metadata = BaseAlchemyModel.metadata

config.set_main_option(
    "sqlalchemy.url",
    get_db_config().pg_dsn + "?async_fallback=True",
)

#db_url = f"postgresql+{get_db_config().DRIVER}://{get_db_config().LOGIN_USER}:{get_db_config().PASSWORD}@{get_db_config().SERVERNAME}/test_db"
#config.set_main_option(
#  "sqlalchemy.url", db_url + "?async_fallback=True",
#)


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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
