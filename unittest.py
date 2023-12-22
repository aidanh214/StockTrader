from main import *
import unittest


if __name__ == "__main__":
    apikey = "W2RO7B9H5RESE4N1"
    stock_data = StockTracker.get_active(apikey)

    # testing getStockDatafromTicker
    # aapl = StockDataHolder.getStockDataFromTicker("AAPL", apikey)
    # print(aapl["2023-10-24"])

    # testing getActiveStocks
    print(stock_data)

