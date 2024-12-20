from fastapi import FastAPI
from uvicorn import run

from src.api_router import router

app = FastAPI(
    title="Wallet Management API",
    description="API for managing user wallets, performing operations (deposits and withdrawals), and querying wallet balances.",
    version="1.0.0"
)
app.include_router(router)
