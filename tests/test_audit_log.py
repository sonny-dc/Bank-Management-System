import unittest

from src import AuditLog, Transaction, TransactionType

class TestAuditLog(unittest.TestCase):
    """
    Test suite for the AuditLog class.
    Verifies that transactions are correctly stored and retrieved.
    """

    def setUp(self):
        self.audit_log = AuditLog()

    def test_initial_state_empty(self):
        """Test that a new audit log contains no transactions."""
        self.assertEqual(len(self.audit_log.transactions), 0)

    def test_log_transaction(self):
        """Test logging a single valid transaction."""
        transaction = Transaction(TransactionType.DEPOSIT, 100.0)
        self.audit_log.log_transaction(transaction)
        
        self.assertEqual(len(self.audit_log.transactions), 1)
        self.assertIn(transaction, self.audit_log.transactions)

    def test_log_multiple_transactions(self):
        """Test logging multiple transactions preserves order."""
        t1 = Transaction(TransactionType.DEPOSIT, 100.0)
        t2 = Transaction(TransactionType.WITHDRAW, 50.0)
        
        self.audit_log.log_transaction(t1)
        self.audit_log.log_transaction(t2)
        
        self.assertEqual(self.audit_log.transactions, [t1, t2])

    def test_log_invalid_object(self):
        """Test that logging a non-Transaction object raises an AssertionError."""
        with self.assertRaises(AssertionError):
            self.audit_log.log_transaction("Not a transaction object")


if __name__ == '__main__':
    unittest.main()