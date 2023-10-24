import json
import urllib.request
import requests
import csv

"""AlphaVantage API Key: """
"""W2RO7B9H5RESE4N1"""

class StockDataHolder(object):
    def __init__(self, apikey):
        self.stocks = self.getActiveStocks(apikey)
        pass

    def getActiveStocks(self, apikey):
        stocks = []
        apicall = "https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=" + apikey
        with requests.Session() as s:
            download = s.get(apicall)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list:
                stocks.append(row)
        return stocks
    def getStockDataFromTicker(ticker, apikey):
        # Get stock data from a ticker symbol using Requests and the AlphaVantage API
        # Input: ticker=String    Output: data=dictionary
        apicall = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&apikey="+apikey
        url = requests.get(apicall)
        dataraw = url.json()
        try:
            data = dataraw["Time Series (Daily)"]
        except KeyError:
            print("KeyError raised in stock data processing, likely an invalid ticker.")
            data = dataraw
        return data

if __name__ == "__main__":
    apikey = "W2RO7B9H5RESE4N1"
    stockData = StockDataHolder(apikey)
    #testing getStockDatafromTicker
    #aapl = StockDataHolder.getStockDataFromTicker("AAPL", apikey)
    #print(aapl["2023-10-24"])

    #testing getActiveStocks
    print(stockData.stocks)
