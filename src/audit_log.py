from .transaction import Transaction


class AuditLog:
    def __init__(self):
        # Audit logs the list of transactions
        self._transactions: list[Transaction] = []

    # Append each transaction to list
    def log_transaction(self, transaction: Transaction) -> None:

        # Ensure only valid Transaction objects are logged
        assert isinstance(transaction, Transaction), "Invalid object logged in AuditLog"

        self._transactions.append(transaction)


    # =======================
    #   Getters (Read-only)
    # =======================

    @property
    def transactions(self) -> list[Transaction]:
        # Return a copy [:] so the internal log cannot be modified externally
        return self._transactions[:]
    
