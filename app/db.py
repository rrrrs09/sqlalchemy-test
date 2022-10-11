from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import app.config as config

AsyncSessionFactory = Callable[..., AsyncSession]


def make_url_async(url: str) -> str:
    """Add +asyncpg to url scheme."""
    return "postgresql+asyncpg" + url[url.find(":") :]


def make_url_sync(url: str) -> str:
    """Remove +asyncpg from url scheme."""
    return "postgresql" + url[url.find(":") :]


Base = declarative_base()


async def build_db_session_factory() -> AsyncSessionFactory:
    engine = create_async_engine(make_url_async(config.POSTGRES_DSN))

    return sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
