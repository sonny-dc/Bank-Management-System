from .audit_log import AuditLog
from .transaction import Transaction, TransactionType
from abc import ABC, abstractmethod


class Account(ABC):
    def __init__(self, account_ID: int):
        self._account_ID: int = account_ID
        self._customer_ID: int | None = None
        self._balance: float = 0
        self._audit_log: AuditLog = AuditLog()


    # Assign account to a customer
    def assign_customer(self, customer_ID: int) -> None:
        if self._customer_ID is not None:
            raise ValueError("Customer already assigned")
        
        self._customer_ID = customer_ID


    # Views Accumulated Transactions
    def view_transaction_history(self) -> list[Transaction]:
        # Accessed as a property (no parentheses)
        return self._audit_log.transactions
    

    def validate_transfer_target(self, destination_account: 'Account') -> None:
        """
        Validates that the destination account is eligible for a transfer.
        This method is exposed to allow the UI/API to 'fail fast'. The transfer() 
        method also calls this internally to ensure data integrity.
        """

        # Ensure the developer passed a valid Account object, not just an ID
        assert isinstance(destination_account, Account), "Destination must be an Account object"
        
        # Prevents circular transfers (A -> A)
        if self == destination_account:
            raise ValueError("Cannot transfer to the same account.")


    # Transfers funds to a designated account
    def transfer(self, destination_account: 'Account', amount: float) -> None:
        """ withdraw logic depends whether it is from Checkings or Savings, since
          this is an abstract class, it works both sides based on their
          unique withdraw functions """

        self.validate_transfer_target(destination_account)

        # transfers to the target acount object using withdraw helper
        self._withdraw_helper(amount, TransactionType.TRANSFER_SENT)

        # transfers to the target account object using deposit helper
        destination_account._deposit_helper(amount, TransactionType.TRANSFER_RECEIVED)


    # Main Deposit function
    def deposit(self, amount: float) -> None:
        self._deposit_helper(amount, TransactionType.DEPOSIT)


    # Deposits designated amount and logs the transaction
    def _deposit_helper(self, amount: float, transaction_type: TransactionType) -> None:
        if amount <= 0:
            raise ValueError("Invalid deposit amount")
        
        # increment balance by amount
        self._balance += amount

        # log the transaction to audit_log
        new_tx: Transaction = Transaction(transaction_type, amount)
        self._audit_log.log_transaction(new_tx)


    # Main Withdraw function
    def withdraw(self, amount: float) -> None:
        self._withdraw_helper(amount, TransactionType.WITHDRAW)


    # Withdraws designated amount and logs the transactions
    @abstractmethod
    def _withdraw_helper(self, amount: float, transaction_type: TransactionType) -> None:
        pass


    # =======================
    #   Getters (Read-only)
    # =======================

    @property
    def balance(self) -> float:
        return self._balance
    
    @property
    def account_ID(self) -> int:
        return self._account_ID
    
    @property
    def customer_ID(self) -> int:
        return self._customer_ID
    

class SavingsAccount(Account):
    def __init__(self, account_ID: int):
        super().__init__(account_ID)
        self.__interest_rate: float = 0.015


    def _withdraw_helper(self, amount: float, transaction_type: TransactionType) -> None:
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount")
        
        if self._balance - amount < 0:
            raise ValueError("Insufficient funds")
        
        self._balance -= amount

        # Ensure the logic above never resulted in a negative balance.
        assert self._balance >= 0, "CRITICAL LOGIC ERROR: Savings balance became negative!"

        new_tx: Transaction = Transaction(transaction_type, amount)
        self._audit_log.log_transaction(new_tx)


    def apply_interest(self) -> None:
        # Rule: Apply interest (1.5%)
        interest: float = self._balance * self.__interest_rate
        if interest > 0:
            self._deposit_helper(interest, TransactionType.INTEREST_APPLIED)


    # =======================
    #   Getters (Read-only)
    # =======================

    @property
    def interest_rate(self) -> float:
        return self.__interest_rate
    
    
class CheckingAccount(Account):
    def __init__(self, account_ID: int):
        super().__init__(account_ID)
        self.__overdraft_limit: float = -500
        self.__overdraft_fee: float = 35


    def _withdraw_helper(self, amount: float, transaction_type: TransactionType) -> None:
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount")
        
        is_negative: bool = self._balance < 0
        
        projected_balance: float = self._balance - amount
        fee: float = 0
        
        # Rule: Apply Overdraft Fee if balance drops below 0
        if projected_balance < 0 and not is_negative:
            fee = self.__overdraft_fee
            
        # Ensure fee is never charged if already negative
        if is_negative:
            assert fee == 0, "Logic Error: Overdraft fee charged on already negative balance"

        if (projected_balance - fee) < self.__overdraft_limit:
            raise ValueError("Overdraft limit exceeded")
        
        # Apply withdraw
        self._balance -= amount

        new_tx: Transaction = Transaction(transaction_type, amount)
        self._audit_log.log_transaction(new_tx)

        # Log the fee as an extra fee
        if fee > 0:
            self._balance -= fee
            new_tx: Transaction = Transaction(TransactionType.EXTRA_FEE, fee)
            self._audit_log.log_transaction(new_tx)

        # Ensure the math above never violated the overdraft limit
        assert self._balance >= self.__overdraft_limit, "CRITICAL LOGIC ERROR: Checking balance below overdraft limit!"


    # =======================
    #   Getters (Read-only)
    # =======================
    
    @property
    def overdraft_limit(self) -> float:
        return self.__overdraft_limit
    
    @property
    def overdraft_fee(self) -> float:
        return self.__overdraft_fee
    
