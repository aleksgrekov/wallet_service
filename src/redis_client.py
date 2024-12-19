import os

import redis.asyncio as redis

client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), db=0, decode_responses=True)


async def get_wallet_from_cache(wallet_uuid: str):
    """
    Get wallet balance from Redis cache.

    Parameters:
        wallet_uuid (str): UUID of the wallet.

    Returns:
        float: Balance of the wallet if found in cache, otherwise None.
    """
    balance = await client.get(wallet_uuid)
    if balance:
        return float(balance)
    return None


async def set_wallet_in_cache(wallet_uuid: str, balance: float):
    """
    Set wallet balance in Redis cache.

    Parameters:
        wallet_uuid (str): UUID of the wallet.
        balance (float): Wallet balance to store.
    """
    await client.set(wallet_uuid, balance)
