import requests
import csv
import tkinter as tk
import datetime
from tkinter import ttk

# AlphaVantage API Key:
# W2RO7B9H5RESE4N1


class SpendingData:
    def __init__(self):
        self.transactions = {}

    def add_transaction(self, date, value, note):
        if (date, note) in self.transactions:
            self.transactions[date, note][2] += value
        else:
            self.transactions[date, note] = [date, note, value]

    def remove_transaction(self, date, note):
        if (date, note) in self.transactions:
            del self.transactions[date,note]
        else:
            raise ValueError("No transaction to delete.")

    def modify_transaction(self, date, note, new_value):
        if (date, note) in self.transactions:
            self.transactions[date, note] = [date, note, new_value]
        else:
            raise ValueError("No transaction to modify.")

    def save_spending(self, user, password):
        pass

    def load_spending(self, user, password):
        pass


class InvestmentData:
    def __init__(self):
        self.portfolio = {}

    def add_asset(self, asset_type):
        if asset_type == "stock":
            pass
        elif asset_type == "bond":
            pass
        elif asset_type == "cash":
            pass
        elif asset_type == "other":
            pass
        else:
            raise ValueError(str("No asset of type: " + asset_type))

    def save_spending(self, user, password):
        pass

    def load_spending(self, user, password):
        pass


if __name__ == "__main__":
    pass