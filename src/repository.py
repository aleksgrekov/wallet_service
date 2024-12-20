from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import Wallet, Operation
from src.redis_client import set_wallet_in_cache


class WalletRepository:
    @classmethod
    async def perform_operation(cls, wallet_uuid: str, operation_type: str, amount: float, db: AsyncSession) -> None:
        try:
            async with db.begin():
                query = select(Wallet).filter(Wallet.uuid == wallet_uuid).with_for_update()
                request = await db.execute(query)
                wallet = request.scalar_one_or_none()

                if not wallet:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

                if operation_type == "DEPOSIT":
                    wallet.balance += amount
                elif operation_type == "WITHDRAW":
                    if wallet.balance < amount:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No enough money")
                    wallet.balance -= amount
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operation type")

                db.add(wallet)

                await set_wallet_in_cache(wallet.uuid, wallet.balance)

                db.add(Operation(wallet_uuid=wallet_uuid, type=operation_type, amount=amount))
                await db.commit()
        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

    @classmethod
    async def get_wallet_with_balance(cls, wallet_uuid: str, db: AsyncSession) -> Wallet:
        query = select(Wallet).filter(Wallet.uuid == wallet_uuid)
        result = await db.execute(query)
        wallet = result.scalar_one_or_none()

        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

        return wallet
