from main import *
import unittest


class TestSpendingData(unittest.TestCase):
    def setUp(self):
        self.spending_data = SpendingData()

    def test_add_transaction(self):
        # Test adding a valid transaction
        self.spending_data.add_transaction("2023-01-01", 100, "Groceries")
        self.assertEqual(self.spending_data.transactions["2023-01-01", "Groceries"], ["2023-01-01", "Groceries", 100])

    def test_remove_transaction(self):
        # Test removing a non-existing transaction (corner case)
        with self.assertRaises(ValueError):
            self.spending_data.remove_transaction("2023-01-01", "Groceries")

        # Test removing an existing transaction
        self.spending_data.add_transaction("2023-01-01", 100, "Groceries")
        self.spending_data.remove_transaction("2023-01-01", "Groceries")
        self.assertNotIn(("2023-01-01", "Groceries"), self.spending_data.transactions)

        # Test removing a non-existing transaction after previous removal (corner case)
        with self.assertRaises(ValueError):
            self.spending_data.remove_transaction("2023-01-01", "Groceries")

    def test_modify_transaction(self):
        # Test modifying an existing transaction
        self.spending_data.add_transaction("2023-01-01", 100, "Groceries")
        self.spending_data.modify_transaction("2023-01-01", "Groceries", 200)
        self.assertEqual(self.spending_data.transactions["2023-01-01", "Groceries"], ["2023-01-01", "Groceries", 200])

        # Test modifying a non-existing transaction (corner case)
        with self.assertRaises(ValueError):
            self.spending_data.modify_transaction("2023-01-02", "Coffee", 50)


if __name__ == '__main__':
    unittest.main()
