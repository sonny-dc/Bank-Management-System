from .transaction import Transaction


class AuditLog:
    def __init__(self):
        self._transactions: list[Transaction] = []

    def log_transaction(self, transaction: Transaction) -> None:

        assert isinstance(transaction, Transaction), "Invalid object logged in AuditLog"

        self._transactions.append(transaction)


    # =======================
    #   Getters (Read-only)
    # =======================

    @property
    def transactions(self) -> list[Transaction]:
        return self._transactions[:]
    
