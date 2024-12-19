from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import create_session
from src.redis_client import get_wallet_from_cache
from src.repository import WalletRepository
from src.schemas import SuccessSchema, OperationSchema, WalletSchema

router = APIRouter(
    prefix="/api/v1/wallets",
    tags=["Wallets"],
)


@router.post(
    "/{wallet_uuid}/operation",
    response_model=SuccessSchema,
    status_code=status.HTTP_200_OK,
    summary="Perform an operation on a wallet",
    description="Performs a deposit or withdrawal operation on the specified wallet. Returns the updated wallet balance.",
    responses={
        200: {"description": "Operation performed successfully"},
        400: {"description": "Bad request (Invalid operation type or insufficient funds or something goes wrong)"},
        404: {"description": "Wallet not found"},
        500: {"description": "Internal server error"},
    }
)
async def perform_wallet_operation(wallet_uuid: str, operation: OperationSchema,
                                   db: AsyncSession = Depends(create_session)) -> SuccessSchema:
    """
    Perform an operation (deposit or withdrawal) on the wallet.

    Parameters:
        wallet_uuid (str): UUID of the wallet for the operation.
        operation (OperationSchema): Operation details (type and amount).
        db (AsyncSession): Asynchronous database session dependency.

    Returns:
        SuccessSchema: Successful operation status.

    Raises:
        HTTPException 404: If the wallet is not found.
        HTTPException 400: If there are insufficient funds for withdrawal or invalid operation type or something goes wrong.
    """
    await WalletRepository.perform_operation(wallet_uuid, operation.operationType, operation.amount, db)
    return SuccessSchema()


@router.get(
    "/{wallet_uuid}",
    response_model=WalletSchema,
    status_code=status.HTTP_200_OK,
    summary="Get wallet balance",
    description="Fetches the balance of the wallet with the specified UUID. First checks Redis cache, then the database.",
    responses={
        200: {"description": "Wallet balance fetched successfully"},
        404: {"description": "Wallet not found"},
        500: {"description": "Internal server error"},
    }
)
async def get_balance(wallet_uuid: str, db: AsyncSession = Depends(create_session)) -> WalletSchema:
    """
    Get the balance of a wallet.

    Parameters:
        wallet_uuid (str): UUID of the wallet.
        db (AsyncSession): Asynchronous database session dependency.

    Returns:
        WalletSchema: The wallet data, including the balance.

    Raises:
        HTTPException 404: If the wallet is not found.
    """
    balance = await get_wallet_from_cache(wallet_uuid)
    if balance is not None:
        return WalletSchema(uuid=wallet_uuid, balance=balance)

    wallet = await WalletRepository.get_wallet_with_balance(wallet_uuid, db)
    return WalletSchema(uuid=wallet.uuid, balance=wallet.balance)
