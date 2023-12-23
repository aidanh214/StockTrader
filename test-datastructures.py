from main import *
import unittest
import tempfile
import sqlite3
import os
from unittest.mock import patch

# Testing framework for the datastructure implementations in main.py
# I used ChatGPT to generate most of this.
# Life is too short for writing hundreds of lines of unit tests.


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

    def test_save_data(self):
        # Add some transactions for testing
        self.spending_data.add_transaction("2023-01-01", 100, "Groceries")
        self.spending_data.add_transaction("2023-01-02", 50, "Dining")
        self.spending_data.add_transaction("2023-01-03", 30, "Shopping")

        # Create a temporary database file for testing
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

            # Save data
            self.spending_data.save_data(temp_filename)

            # Check if the data is saved correctly
            con = sqlite3.connect(temp_filename)
            cur = con.cursor()
            saved_data = cur.execute("SELECT * FROM spending").fetchall()

            expected_data = [
                ('2023-01-01', 'Groceries', 100),
                ('2023-01-02', 'Dining', 50),
                ('2023-01-03', 'Shopping', 30)
            ]

            self.assertEqual(saved_data, expected_data)

            # Clean up the temporary file
            temp_file.close()
            os.remove(temp_filename)

    def test_load_data(self):
        # Set up a known state of the data
        self.spending_data.add_transaction("2023-01-01", 100, "Groceries")
        self.spending_data.add_transaction("2023-01-02", 50, "Dining")
        self.spending_data.add_transaction("2023-01-03", 30, "Shopping")

        # Create a temporary database file for testing
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

            # Save data
            self.spending_data.save_data(temp_filename)

            # Clear the existing data in the SpendingData instance
            self.spending_data = SpendingData()

            # Load data
            self.spending_data.load_data(temp_filename)

            # Check if the loaded data matches the expected state
            expected_data = {
                ('2023-01-01', 'Groceries'): ['2023-01-01', 'Groceries', 100],
                ('2023-01-02', 'Dining'): ['2023-01-02', 'Dining', 50],
                ('2023-01-03', 'Shopping'): ['2023-01-03', 'Shopping', 30]
            }

            self.assertEqual(self.spending_data.transactions, expected_data)

            # Clean up the temporary file
            temp_file.close()
            os.remove(temp_filename)
class TestInvestmentData(unittest.TestCase):
    def setUp(self):
        self.investment_data = InvestmentData()

    def tearDown(self):
        pass

    @patch('sqlite3.connect')
    def test_add_asset(self, mock_connect):
        # Test adding stock
        self.investment_data.add_asset("stock", 10, "AAPL")
        self.assertEqual(self.investment_data.portfolio, {("stock", "AAPL"): 10})

        # Test adding bond
        self.investment_data.add_asset("bond", 5, "Government")
        self.assertEqual(self.investment_data.portfolio, {("stock", "AAPL"): 10, ("bond", "Government"): 5})

        # Test adding cash
        self.investment_data.add_asset("cash", 1000)
        self.assertEqual(self.investment_data.portfolio, {("stock", "AAPL"): 10, ("bond", "Government"): 5, ("cash", ""): 1000})

    def test_save_load_data(self):
        # Set up a mock portfolio
        self.investment_data.portfolio = {("stock", "AAPL"): 10, ("bond", "Government"): 5, ("cash", ""): 1000}

        # Create a temporary database file for testing
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

            # Save data
            self.investment_data.save_data(temp_filename)

            # Create a new InvestmentData instance and load data from the file
            new_investment_data = InvestmentData()
            new_investment_data.load_data(temp_filename)

            # Check if the loaded data matches the original data
            self.assertEqual(self.investment_data.portfolio, new_investment_data.portfolio)

            # Clean up the temporary file
            temp_file.close()
            os.remove(temp_filename)

if __name__ == '__main__':
    unittest.main()


