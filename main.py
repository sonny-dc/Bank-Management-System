# Main Class
from src import Customer, SavingsAccount, CheckingAccount


# ================
# Helper Functions
# ================

def check_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def check_str(prompt: str, alpha_only: bool = False) -> str:
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise ValueError("Input cannot be empty")
            
            if alpha_only and not value.isalpha():
                raise ValueError("Input must contain only letters")

            return value
        
        except ValueError as e:
            print(f"Invalid input. {e}")


def process_transaction(prompt: str, transaction_func) -> float | None:
    while True:
        user_input = input(f"{prompt} (or 'e' to cancel): ").strip()
        if user_input.lower() == 'e':
            print("Transaction canceled.")
            return None

        try:
            amount = float(user_input)
            
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        try:
            transaction_func(amount)
            return amount
        except ValueError as e:
            print(f"Error: {e}")


def transfer_process(customer: Customer, account: SavingsAccount | CheckingAccount) -> None:
    # Optimization: Store accounts list once to avoid creating multiple copies
    accounts = customer.accounts
    if len(accounts) <= 1:
        print("There's no account to transfer to! You only have one account!")
        return

    print("----Transfer----")
    print("Available Accounts:")
    for acc in accounts:
        print(f"Account ID: {acc.account_ID} ({type(acc).__name__})")

    while True:
        destination_account_ID = check_int("Enter destination account ID: ")
        destination_account = customer.get_account(destination_account_ID)

        if not destination_account:
            print("Destination account not found.")
            continue

        try:
            account.validate_transfer_target(destination_account)
        except ValueError as e:
            print(f"Error: {e}")
            continue

        amount = process_transaction("Enter transfer amount", lambda amt: account.transfer(destination_account, amt))
        if amount:
            print(f"Transfer of ${amount} successful!")
        
        # Exit the transfer loop whether successful or cancelled
        break


def show_transaction_history(account: SavingsAccount | CheckingAccount) -> None:
    transaction_history = account.view_transaction_history()
    if not transaction_history:
        print("No transaction history available.")
        return

    print("Transaction History:")
    for transaction in transaction_history:
        print(f"{transaction.timestamp} - {transaction.transaction_type.value} - ${transaction.amount}")


def choose_account(customer: Customer) -> SavingsAccount | CheckingAccount | None:
    # Optimization: Store accounts list once
    accounts = customer.accounts
    if not accounts:
        print("No accounts available, please create one first!")
        return None
    
    print("Available Accounts:")

    for account in accounts:
        print(f"Account ID: {account.account_ID} ({type(account).__name__})")
        
    account = customer.get_account(check_int("Enter Account ID: "))

    if not account:
        print("Account ID not found.")
        return None
    
    return account


def create_customer() -> Customer:
    cust_ID: int = check_int("Enter Customer ID: ")
    first_name: str = check_str("Enter First Name: ", alpha_only=True)
    last_name: str = check_str("Enter Last Name: ", alpha_only=True)
    email: str = check_str("Enter Email: ")

    return Customer(cust_ID, first_name, last_name, email)


def create_checking_account(customer: Customer) -> CheckingAccount:
    while True:
        account_ID: int = check_int("Enter Checking Account ID: ")
        
        # Optimization: Use get_account to check existence (avoids copying the list)
        if customer.get_account(account_ID):
            print(f"Account ID {account_ID} is already taken. Please try again.")
            continue
        
        return CheckingAccount(account_ID)


def create_savings_account(customer: Customer) -> SavingsAccount:
    while True:
        account_ID: int = check_int("Enter Savings Account ID: ")
        
        if customer.get_account(account_ID):
            print(f"Account ID {account_ID} is already taken. Please try again.")
            continue
            
        return SavingsAccount(account_ID)
         

def open_account(customer: Customer) -> None:
    while True:
        print("What type of account do you want to create?")
        answer = check_str("Savings or Checking?(s/c): ").lower()
        if answer == "s":
            account = create_savings_account(customer)
            customer.open_account(account)
            print(f"Savings Account (ID: {account.account_ID}) opened successfully!")

        elif answer == "c":
            account = create_checking_account(customer)
            customer.open_account(account)
            print(f"Checking Account (ID: {account.account_ID}) opened successfully!")
            
        else:
            print("Invalid input! enter 's' or 'c'")
            continue

        return


# ================ ^
# Helper Functions |
# ================ |

def account_manager(customer: Customer, account: SavingsAccount | CheckingAccount) -> None:
    while True:
        print("----Account Manager----")
        print(f"Account ID: {account.account_ID}")
        print(f"Account Type: {type(account).__name__}")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. View Transaction History")
        print("5. View Balance")
        print("6. Exit")
        answer = check_int("Enter your choice: ")
        if answer == 1:
            amount = process_transaction("Enter deposit amount", account.deposit)
            if amount:
                print(f"Deposit of ${amount} successful!")
            
        elif answer == 2:
            amount = process_transaction("Enter withdrawal amount", account.withdraw)
            if amount:
                print(f"Withdrawal of ${amount} successful!")

        elif answer == 3:
            transfer_process(customer, account)

        elif answer == 4:
            show_transaction_history(account)
        
        elif answer == 5:
            print(f"Current Balance: ${account.balance}")

        elif answer == 6:
            print("Exiting account manager...")
            return
        

def secure_bank_interface() -> None:

    print("********Welcome to SecureBank!********")
    while True:
        answer = input("Do you want to apply for an account?(y/n): ").lower().strip()
        if answer == "y":
            customer = create_customer()
            break
        elif answer == "n":
            print("Exiting SecureBank...")
            return
        else:
            print("Invalid input! enter 'y' or 'n'")
            continue
    
    while True:
        print("----Customer Choices----")
        print("1. Open an account")
        print("2. Choose an account to use (shows current account IDs and input the one you'll use)")
        print("3. Exit")
        answer = check_int("Enter your choice: ")
        if answer == 1:
            open_account(customer)

        elif answer == 2:
            account = choose_account(customer)
            if account:
                account_manager(customer, account)

        elif answer == 3:
            print("Exiting SecureBank...")
            return


def main():
    secure_bank_interface()


if __name__ == '__main__':
    main()
