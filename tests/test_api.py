import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Wallet
from src.schemas import OperationSchema


@pytest.mark.asyncio
async def test_get_wallet_balance(ac: AsyncClient, wallet: Wallet):
    """Test to fetch wallet balance"""
    response = await ac.get(f"/api/v1/wallets/{wallet.uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "uuid": wallet.uuid,
        "balance": wallet.balance,
        "message": "Operation successful",
    }


@pytest.mark.asyncio
async def test_wallet_deposit(ac: AsyncClient, wallet: Wallet, db: AsyncSession):
    """Test deposit operation"""
    operation = OperationSchema(operationType="DEPOSIT", amount=50.0)
    response = await ac.post(
        f"/api/v1/wallets/{wallet.uuid}/operation", json=operation.model_dump()
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Operation successful"}

    await db.refresh(wallet)

    db_wallet = await db.execute(select(Wallet).filter(Wallet.uuid == wallet.uuid))
    db_wallet = db_wallet.scalar_one_or_none()
    assert db_wallet.balance == 150.0


@pytest.mark.asyncio
async def test_wallet_withdrawal(ac: AsyncClient, wallet: Wallet, db: AsyncSession):
    """Test withdrawal operation"""
    operation = OperationSchema(operationType="WITHDRAW", amount=30.0)
    response = await ac.post(
        f"/api/v1/wallets/{wallet.uuid}/operation", json=operation.model_dump()
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Operation successful"}

    await db.refresh(wallet)

    query = select(Wallet).filter(Wallet.uuid == wallet.uuid)
    db_wallet = await db.execute(query)
    db_wallet = db_wallet.scalars().one_or_none()
    assert db_wallet.balance == 70.0


@pytest.mark.asyncio
async def test_wallet_withdrawal_no_money(
    ac: AsyncClient, wallet: Wallet
):
    """Test withdrawal with no enough money"""
    operation = OperationSchema(operationType="WITHDRAW", amount=200.0)
    response = await ac.post(
        f"/api/v1/wallets/{wallet.uuid}/operation", json=operation.model_dump()
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "No enough money"}


@pytest.mark.asyncio
async def test_wallet_not_found(ac: AsyncClient):
    """Test case when wallet is not found"""
    response = await ac.get("/api/v1/wallets/non-existing-uuid")

    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}


@pytest.mark.asyncio
async def test_perform_invalid_operation_type(ac: AsyncClient, wallet: Wallet):
    """Test case when operation type is invalid"""
    operation = OperationSchema(operationType="INVALID", amount=100.0)
    response = await ac.post(
        f"/api/v1/wallets/{wallet.uuid}/operation", json=operation.model_dump()
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid operation type"}