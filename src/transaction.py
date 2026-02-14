from enum import Enum
from datetime import datetime


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER_SENT = "TRANSFER SENT"
    TRANSFER_RECEIVED = "TRANSFER RECEIVED"
    INTEREST_APPLIED = "INTEREST APPLIED"
    EXTRA_FEE = "EXTRA FEE"


class Transaction:
    def __init__(self, transaction_type: TransactionType, amount: float):
        
        if amount <= 0:
            raise ValueError("Invalid transaction amount")
        
        self._transaction_type: TransactionType = transaction_type
        self._amount: float = amount
        self._timestamp: datetime = datetime.now()


    # =======================
    #   Getters (Read-only)
    # =======================

    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __repr__(self) -> str:
        return f"Transaction(type={self._transaction_type.name}, amount={self._amount}, time={self._timestamp})"
    
