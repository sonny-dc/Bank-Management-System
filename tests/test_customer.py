import unittest

from src import Customer, SavingsAccount, CheckingAccount

class TestCustomer(unittest.TestCase):
    """
    Test suite for the Customer class.
    """

    def setUp(self):
        self.customer = Customer(1, "John", "Doe", "john@example.com")

    def test_customer_creation(self):
        """Test that a customer is created with the correct attributes."""
        self.assertEqual(self.customer.customer_ID, 1)
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.email, "john@example.com")
        self.assertEqual(self.customer.accounts, [])

    def test_open_account(self):
        """Test that opening an account links it to the customer."""
        account = SavingsAccount(101)
        self.customer.open_account(account)

        # Verify the account is stored in the customer's list
        self.assertEqual(self.customer.get_account(101), account)
        # Verify the customer ID was assigned to the account
        self.assertEqual(account.customer_ID, 1)

    def test_get_account_returns_none_if_not_found(self):
        """Test that searching for a non-existent account returns None."""
        account = CheckingAccount(202)
        self.customer.open_account(account)

        found = self.customer.get_account(999) # Random ID
        self.assertIsNone(found)

    def test_open_account_already_assigned_fails(self):
        """Test that a customer cannot open an account already owned by someone else."""
        account = SavingsAccount(303)
        
        # Assign to another customer first
        other_customer = Customer(2, "Jane", "Doe", "jane@example.com")
        other_customer.open_account(account)

        # Try to assign to current customer
        with self.assertRaises(ValueError):
            self.customer.open_account(account)


if __name__ == '__main__':
    unittest.main()