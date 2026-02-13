import sys
import os
import unittest

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import SavingsAccount

class TestSavingsAccount(unittest.TestCase):
    """
    Test suite for the SavingsAccount class.
    Verifies business rules:
    1. No overdrafts allowed (balance cannot go negative).
    2. Interest application works correctly (1.5%).
    3. Standard deposit/withdraw operations.
    """

    def setUp(self):
        """Runs before EVERY test. Sets up a clean account with $100."""
        self.account = SavingsAccount(1000)
        self.account.deposit(100.0)
    
    def test_deposit_valid(self):
        """Test that money is added correctly to the balance."""
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)

    def test_deposit_negative_amount(self):
        """Test that we cannot deposit a negative amount."""
        with self.assertRaises(ValueError):
            self.account.deposit(-50.0)

    def test_deposit_zero_amount(self):
        """Test that depositing zero is not allowed."""
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_withdraw_valid(self):
        """Test that money is removed correctly when funds are sufficient."""
        self.account.withdraw(40.0)
        self.assertEqual(self.account.balance, 60.0)

    def test_withdraw_insufficient_funds(self):
        """
        Test the Business Rule: Savings cannot go negative.
        We expect a ValueError if withdrawal exceeds balance.
        """
        with self.assertRaises(ValueError):
            self.account.withdraw(101.0) # Trying to withdraw more than $100

    def test_withdraw_exact_balance(self):
        """Test withdrawing the entire balance, resulting in zero."""
        self.account.withdraw(100.0)
        self.assertEqual(self.account.balance, 0)

    def test_withdraw_negative_amount(self):
        """Test that we cannot withdraw negative numbers."""
        with self.assertRaises(ValueError):
            self.account.withdraw(-10.0)

    def test_apply_interest(self):
        """
        Test that interest is calculated and deposited correctly.
        Rate is 1.5% (0.015). Balance: 100 -> Interest: 1.5 -> New Balance: 101.5.
        """
        self.account.apply_interest()
        self.assertEqual(self.account.balance, 101.5)

    def test_apply_interest_on_zero_balance(self):
        """Test that no interest is applied if the balance is zero."""
        self.account.withdraw(100.0) # Make balance zero
        self.account.apply_interest()
        self.assertEqual(self.account.balance, 0)

    def test_transfer_valid(self):
        """Test transferring money to another account."""
        recipient = SavingsAccount(2000)
        self.account.transfer(recipient, 40.0)
        self.assertEqual(self.account.balance, 60.0)
        self.assertEqual(recipient.balance, 40.0)

    def test_transfer_fail_insufficient_funds(self):
        """Test that transfer fails if savings would go negative."""
        recipient = SavingsAccount(2000)
        with self.assertRaises(ValueError):
            self.account.transfer(recipient, 150.0)
        
        # Verify atomicity: sender balance unchanged, recipient gets nothing
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(recipient.balance, 0.0)
    
if __name__ == '__main__':
    unittest.main()