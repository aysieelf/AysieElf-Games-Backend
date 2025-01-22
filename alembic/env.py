from logging.config import fileConfig
import os

from alembic import context
from src.core.config import settings

# ruff: noqa: F401
from src.models.base import Base
from src.models.blacklisted_token import BlacklistedToken
from src.models.category import Category
from src.models.favorite import Favorite
from src.models.friendship import Friendship
from src.models.game import Game
from src.models.game_activity import GameActivity
from src.models.upvote import Upvote
from src.models.user import User

from sqlalchemy import engine_from_config, pool

target_metadata = Base.metadata


def get_url():
    return settings.DATABASE_URL


config = context.config
config.set_main_option("sqlalchemy.url", get_url())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


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


def run_migrations_online():
    engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        url=settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
