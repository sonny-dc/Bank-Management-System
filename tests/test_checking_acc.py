import sys
import os
import unittest

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import CheckingAccount

class TestCheckingAccount(unittest.TestCase):

    def setUp(self):
        self.account = CheckingAccount(123)
        self.account.deposit(100.0)

    def test_withdraw_valid(self):
        """Test a standard withdrawal that is within the positive balance."""
        self.account.withdraw(50.0)
        self.assertEqual(self.account.balance, 50.0)

    def test_overdraft_fee_applied(self):
        """
        Test that the 35$ fee is applied when going below zero.
        Start: 100$
        Withdraw: 150$
        Math: 100 - 150 = -50
        Fee = -35
        Result: -85
        """

        self.account.withdraw(150.0)
        self.assertEqual(self.account.balance, -85.0)

    def test_overdraft_limit_exceeded(self):
        """Test that we cannot go beyond -500 limit."""
        # Balance is 100. Limit is -500. Total available swing is 600.
        # Trying to withdraw 700 should fail.
        with self.assertRaises(ValueError):
            self.account.withdraw(700.0)


    def test_no_extra_fee_if_already_negative(self):
        """
        Test the logic we just fixed:
        If already negative, do NOT charge the 35$ fee again.
        """

        # 1. Go negative first
        self.account.withdraw(150.0) # balance becomes -85 (100 - 150 - 35)

        # 2. Withdraw again (within limit)
        # Current: -85, Withdraw: 10.
        # Expected: -95, (No extra 35$ fee)
        self.account.withdraw(10.0)
        self.assertEqual(self.account.balance, -95.0)

    def test_deposit_negative_amount(self):
        """Test that we cannot deposit a negative amount."""
        with self.assertRaises(ValueError):
            self.account.deposit(-50.0)

    def test_deposit_zero_amount(self):
        """Test that depositing zero is not allowed."""
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_withdraw_negative_amount(self):
        """Test that we cannot withdraw negative numbers."""
        with self.assertRaises(ValueError):
            self.account.withdraw(-10.0)

    def test_withdraw_exact_balance_to_zero(self):
        """Test withdrawing exact balance results in 0 and no fee."""
        self.account.withdraw(100.0)
        self.assertEqual(self.account.balance, 0.0)

    def test_withdraw_exact_overdraft_limit(self):
        """
        Test hitting the exact overdraft limit.
        Balance: 100. Limit: -500. Fee: 35.
        Max withdraw = 100 + 500 - 35 = 565.
        Resulting Balance = 100 - 565 - 35 = -500.
        """
        self.account.withdraw(565.0)
        self.assertEqual(self.account.balance, -500.0)

    def test_withdraw_just_over_limit(self):
        """Test withdrawing just 1 cent over the limit fails."""
        with self.assertRaises(ValueError):
            self.account.withdraw(565.01)

    def test_transfer_valid(self):
        """Test transferring money to another account."""
        recipient = CheckingAccount(456)
        self.account.transfer(recipient, 50.0)
        self.assertEqual(self.account.balance, 50.0)
        self.assertEqual(recipient.balance, 50.0)

    def test_transfer_triggers_overdraft(self):
        """Test that a transfer can trigger an overdraft fee on the sender."""
        recipient = CheckingAccount(456)
        # Balance 100. Transfer 150.
        # Logic: 100 - 150 = -50. Fee = 35. Final = -85.
        self.account.transfer(recipient, 150.0)
        
        self.assertEqual(self.account.balance, -85.0)
        self.assertEqual(recipient.balance, 150.0)

    def test_transfer_exceeds_overdraft_limit(self):
        """Test that transfer fails if it exceeds the overdraft limit."""
        recipient = CheckingAccount(456)
        with self.assertRaises(ValueError):
            self.account.transfer(recipient, 1000.0)

if __name__ == '__main__':
    unittest.main()
