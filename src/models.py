from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    """
    Model representing a wallet in the database.

    Attributes:
        uuid (str): Unique identifier of the wallet.
        balance (float): The balance of the wallet, default is 0.0.
    """
    __tablename__ = 'wallets'

    uuid: Mapped[str] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(default=0.0)


class Operation(Base):
    """
    Model representing a transaction or operation on a wallet.

    Attributes:
        id (int): Unique identifier of the operation.
        wallet_uuid (str): UUID of the wallet related to the operation.
        type (str): Type of the operation (DEPOSIT or WITHDRAW).
        amount (float): Amount involved in the operation.
    """
    __tablename__ = 'operations'

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_uuid: Mapped[str]
    type: Mapped[str]
    amount: Mapped[float]
