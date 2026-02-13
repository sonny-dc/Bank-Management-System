import unittest
import sys
import os
from datetime import datetime

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import Transaction, TransactionType

class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        """
        Test that a transaction is created with the correct attributes.
        """
        transaction = Transaction(TransactionType.DEPOSIT, 100.0)
        self.assertEqual(transaction.transaction_type, TransactionType.DEPOSIT)
        self.assertEqual(transaction.amount, 100.0)
        self.assertIsNotNone(transaction.timestamp)

    def test_invalid_transaction_amount(self):
        """Test that creating a transaction with negative/zero amount raises ValueError"""
        with self.assertRaises(ValueError):
            Transaction(TransactionType.DEPOSIT, -100.0)

        with self.assertRaises(ValueError):
            Transaction(TransactionType.DEPOSIT, 0)

    def test_all_transaction_types(self):
        """Test that all defined transaction types work correctly."""
        for t_type in TransactionType:
            transaction = Transaction(t_type, 50.0)
            self.assertEqual(transaction.transaction_type, t_type)

    def test_timestamp_validity(self):
        """Test that the timestamp is a valid datetime object."""
        transaction = Transaction(TransactionType.DEPOSIT, 100.0)
        self.assertIsInstance(transaction.timestamp, datetime)

    def test_immutability(self):
        """Test that transaction attributes are read-only (immutable)."""
        transaction = Transaction(TransactionType.DEPOSIT, 100.0)
        # Try to modify the amount, which should fail because there is no setter
        with self.assertRaises(AttributeError):
            transaction.amount = 500.0


if __name__ == '__main__':
    unittest.main()