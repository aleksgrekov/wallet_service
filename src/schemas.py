from pydantic import BaseModel, Field


class SuccessSchema(BaseModel):
    message: str = Field(
        default="Operation successful",
        title="Success Response Message",
        description="A message indicating that the operation was successful."
    )


class WalletSchema(SuccessSchema):
    uuid: str = Field(
        ...,
        title="Wallet UUID",
        description="A unique identifier for the wallet."
    )
    balance: float = Field(
        ...,
        title="Wallet Balance",
        description="The current balance of the wallet."
    )

    class Config:
        from_attributes = True


class OperationSchema(BaseModel):
    operationType: str = Field(
        ...,
        title="Operation Type",
        description="The type of operation to be performed on the wallet. Can be either 'DEPOSIT' or 'WITHDRAW'."
    )
    amount: float = Field(
        ...,
        title="Operation Amount",
        description="The amount to be deposited or withdrawn from the wallet."
    )