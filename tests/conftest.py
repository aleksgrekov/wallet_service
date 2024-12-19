from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from main import app
from src.database import create_session
from src.models import Base, Wallet
from src.redis_client import client

engine_test = create_async_engine("sqlite+aiosqlite:///./test.db", echo=True, poolclass=StaticPool)
session_test = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
    expire_on_commit=False
)


async def override_get_db():
    async with session_test() as session:
        yield session


app.dependency_overrides[create_session] = override_get_db


async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def teardown_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def db():
    await setup_db()

    yield session_test()

    await teardown_db()


@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def wallet(db: AsyncSession):
    new_wallet = Wallet(uuid="1234-5678", balance=100.0)
    db.add(new_wallet)
    await db.commit()
    return new_wallet


@pytest.fixture(scope="function", autouse=True)
async def clear_cache():
    await client.delete("1234-5678")
