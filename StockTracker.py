import requests
import csv
import pandas_datareader as pdr

# Implementation for data collection of the StockTrader project. StockTracker data structure is a wrapper around the
# dictionary, with extra functions to update a stock ticker and refresh all stock data at once.
# No longer in use - project pivot. Needs to be removed when more project bones in other areas are complete.

def get_active_stocks():


def get_active_stocks(apikey):
    # Gets list of stocks currently active on the market using the AlphaVantage API
    stocks = []
    apicall = "https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=" + apikey
    with requests.Session() as s:
        download = s.get(apicall)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            # stocks.append([row[0],row[1]])
            stocks.append(row)
    return stocks


def get_stock_data(ticker, apikey):
    # Get stock data from a ticker symbol using Requests and the AlphaVantage API
    # Input: ticker=String    Output: data=dictionary
    apicall = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=" + apikey
    url = requests.get(apicall)
    data_raw = url.json()
    try:
        data = data_raw["Time Series (Daily)"]
    except KeyError:
        print("KeyError raised in stock data processing, likely an invalid ticker.")
        raise
    return data


class StockTracker:
    # StockTracker data type, uses a dictionary mapping ticker: value.

    def __init__(self, active_stocks):
        self.data = {}
        self.stock_data = active_stocks

    def refresh(self, active_stocks):
        self.stock_data = active_stocks

    def add_ticker(self, ticker):
        pass

    def remove_ticker(self, ticker):
        pass
