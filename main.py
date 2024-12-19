from fastapi import FastAPI
from uvicorn import run

from src.api_router import router

app = FastAPI(
    title="Wallet Management API",
    description="API for managing user wallets, performing operations (deposits and withdrawals), and querying wallet balances.",
    version="1.0.0"
)
app.include_router(router)

if __name__ == '__main__':
    run("main:app", port=8000, host='127.0.0.1', reload=True)
