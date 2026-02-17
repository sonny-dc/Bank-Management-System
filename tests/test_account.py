import unittest

from src import Account

# Create concrete implementation of Account for testing purposes
# We need this because we cannot instantiate the Account class directly because it is an Abstract class
class ConcreteAccount(Account):
    """
    A concrete implementation of the abstract Account class.
    Used solely for testing shared logic like transfers and customer assignment.
    """
    def _withdraw_helper(self, amount: float, transaction) -> None:
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount



class TestAccount(unittest.TestCase):
    """
    Test suite for the abstract Account class.
    Verifies shared behavior: Customer assignment and Transfers.
    """

    def setUp(self):
        self.acc1 = ConcreteAccount(1)
        self.acc2 = ConcreteAccount(2)

    def test_cannot_instantiate_abstract_class(self):
        """Test that Python prevents creating an instance of the abstract Account class."""
        with self.assertRaises(TypeError):
            account = Account(1)

    def test_assign_customer(self):
        """Test that a customer ID can be assigned to an account."""
        self.acc1.assign_customer(101)
        self.assertEqual(self.acc1.customer_ID, 101)

    def test_assign_customer_reassignment(self):
        """Test that assigning a customer to an already owned account fails."""
        self.acc1.assign_customer(101)
        with self.assertRaises(ValueError):
            self.acc1.assign_customer(999)

    def test_transfer_valid(self):
        """Test a successful money transfer between two accounts."""
        self.acc1.deposit(100.0)

        self.acc1.transfer(self.acc2, 50.0)

        self.assertEqual(self.acc1.balance, 50.0)
        self.assertEqual(self.acc2.balance, 50.0)

    def test_transfer_insufficient_funds(self):
        """Test that transfer fails if the source account has insufficient funds."""
        self.acc1.deposit(100.0)

        with self.assertRaises(ValueError):
            self.acc1.transfer(self.acc2, 200.0)

        self.assertEqual(self.acc1.balance, 100.0)
        self.assertEqual(self.acc2.balance, 0.0)


if __name__ == '__main__':
    unittest.main()
    
