from .account import Account


class Customer:
    def __init__(self, customer_ID: int, first_name: str, last_name: str, email: str):
        self._customer_ID: int = customer_ID
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._email: str = email
        self._accounts: list[Account] = []

    def open_account(self, account: Account) -> None:

        account.assign_customer(self.customer_ID)

        assert account.customer_ID == self.customer_ID, "Account assignment failed"
        
        self._accounts.append(account)


    def get_account(self, account_ID: int) -> Account | None:
        for account in self._accounts:
            if account.account_ID == account_ID:
                return account
        
        return None
    

    # =======================
    #   Getters (Read-only)
    # =======================
    
    @property
    def customer_ID(self) -> int:
        return self._customer_ID

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def accounts(self) -> list[Account]:
        return self._accounts[:]

    