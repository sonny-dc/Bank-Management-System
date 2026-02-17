import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

import main
from src import Customer, SavingsAccount, CheckingAccount

class TestMain(unittest.TestCase):

    # ==========================
    # Test Helper Functions
    # ==========================

    @patch('builtins.input', side_effect=['abc', '123'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_int_retry(self, mock_stdout, mock_input):
        """Test that check_int rejects non-integers and retries."""
        result = main.check_int("Enter number: ")
        
        self.assertEqual(result, 123)
        # Verify it printed an error message for the first input
        self.assertIn("Invalid input", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['', '123', 'John'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_str_validation(self, mock_stdout, mock_input):
        """Test check_str with alpha_only=True rejects empty strings and numbers."""
        result = main.check_str("Enter name: ", alpha_only=True)
        
        self.assertEqual(result, "John")
        output = mock_stdout.getvalue()
        self.assertIn("Input cannot be empty", output)
        self.assertIn("Input must contain only letters", output)

    # ==========================
    # Test Transaction Processor
    # ==========================

    @patch('builtins.input', side_effect=['100'])
    def test_process_transaction_success(self, mock_input):
        """Test a successful transaction execution."""
        mock_func = MagicMock()
        
        amount = main.process_transaction("Deposit", mock_func)
        
        self.assertEqual(amount, 100.0)
        mock_func.assert_called_once_with(100.0)

    @patch('builtins.input', side_effect=['e'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_process_transaction_cancel(self, mock_stdout, mock_input):
        """Test cancelling a transaction."""
        mock_func = MagicMock()
        
        amount = main.process_transaction("Deposit", mock_func)
        
        self.assertIsNone(amount)
        mock_func.assert_not_called()
        self.assertIn("Transaction canceled.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['-50', 'e'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_process_transaction_handles_error(self, mock_stdout, mock_input):
        """
        Test that if the transaction function raises a ValueError (e.g., negative amount),
        the processor catches it and asks for input again (we cancel with 'e' here).
        """
        def fail_on_negative(amount):
            if amount < 0:
                raise ValueError("Negative amount not allowed")

        main.process_transaction("Deposit", fail_on_negative)
        
        self.assertIn("Error: Negative amount not allowed", mock_stdout.getvalue())

    # ==========================
    # Test Business Logic Flows
    # ==========================

    @patch('builtins.input', side_effect=['1', 'John', 'Doe', 'john@test.com'])
    def test_create_customer(self, mock_input):
        """Test customer creation flow."""
        customer = main.create_customer()
        
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer._customer_ID, 1)
        self.assertEqual(customer._first_name, 'John')

    @patch('sys.stdout', new_callable=StringIO)
    def test_transfer_process_single_account(self, mock_stdout):
        """Test that transfer aborts if customer has only 1 account."""
        cust = Customer(1, "A", "B", "C")
        acc1 = CheckingAccount(101)
        cust.open_account(acc1)

        main.transfer_process(cust, acc1)
        
        self.assertIn("You only have one account", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['202', '50']) # Dest ID: 202, Amount: 50
    @patch('sys.stdout', new_callable=StringIO)
    def test_transfer_process_success(self, mock_stdout, mock_input):
        """Test a full successful transfer flow."""
        # Setup: Customer with 2 accounts
        cust = Customer(1, "A", "B", "C")
        sender = CheckingAccount(101)
        receiver = SavingsAccount(202)
        
        cust.open_account(sender)
        cust.open_account(receiver)
        
        sender.deposit(100.0) # Fund the sender

        # Run Transfer
        main.transfer_process(cust, sender)

        # Verify Balances
        self.assertEqual(sender.balance, 50.0)
        self.assertEqual(receiver.balance, 50.0)
        self.assertIn("Transfer of $50.0 successful!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_transaction_history(self, mock_stdout):
        """Test display of transaction history."""
        acc = SavingsAccount(1)
        acc.deposit(100.0)
        
        main.show_transaction_history(acc)
        
        output = mock_stdout.getvalue()
        self.assertIn("Transaction History:", output)
        self.assertIn("DEPOSIT", output)
        self.assertIn("$100.0", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_transaction_history_empty(self, mock_stdout):
        acc = SavingsAccount(1)
        main.show_transaction_history(acc)
        self.assertIn("No transaction history available", mock_stdout.getvalue())

    # ==========================
    # Test Account Creation & Selection
    # ==========================

    @patch('builtins.input', side_effect=['101'])
    def test_create_checking_account(self, mock_input):
        """Test creating a checking account."""
        cust = Customer(1, "Test", "User", "test@test.com")
        acc = main.create_checking_account(cust)
        self.assertIsInstance(acc, CheckingAccount)
        self.assertEqual(acc.account_ID, 101)

    @patch('builtins.input', side_effect=['202'])
    def test_create_savings_account(self, mock_input):
        """Test creating a savings account."""
        cust = Customer(1, "Test", "User", "test@test.com")
        acc = main.create_savings_account(cust)
        self.assertIsInstance(acc, SavingsAccount)
        self.assertEqual(acc.account_ID, 202)

    @patch('builtins.input', side_effect=['101'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_choose_account_valid(self, mock_stdout, mock_input):
        """Test choosing an existing account."""
        cust = Customer(1, "Test", "User", "test@test.com")
        acc = CheckingAccount(101)
        cust.open_account(acc)
        
        result = main.choose_account(cust)
        self.assertEqual(result, acc)

    @patch('builtins.input', side_effect=['s', '303'])
    def test_open_account_savings(self, mock_input):
        """Test opening a savings account via the menu."""
        cust = Customer(1, "Test", "User", "test@test.com")
        main.open_account(cust)
        
        self.assertEqual(len(cust.accounts), 1)
        self.assertIsInstance(cust.accounts[0], SavingsAccount)
        self.assertEqual(cust.accounts[0].account_ID, 303)

if __name__ == '__main__':
    unittest.main()