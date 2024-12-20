import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DATABASE_CONNECTION')}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def create_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get an async SQLAlchemy session.

    This is used in FastAPI to inject the database session into route handlers.

    Returns:
        AsyncSession: An async session for interacting with the database.
    """
    async with async_session() as session:
        yield session
