import requests, datetime
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

#function to fetch symbol name
def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']

#function to fetch stock data based on user input symbol
def fetch_stock(request):
    stock_symbol = request.GET['tickerSymbol']
    #uses alphavantage stock api to fetch latest stock data in time series
    getStock = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_symbol + '&apikey=R2CDNLQSS8YOEHZU')

    #ensure response status is OK (in case of network issues)
    if (getStock.status_code == 200):
        #fetch stock data in JSON and then get current and previous closing data
        stock = getStock.json()
        stockData = stock['Time Series (Daily)']
        dataForToday = stockData[list(stockData)[0]]
        dataForYesterday = stockData[list(stockData)[1]]

        #compute differences between current & previous closing stock prices
        closingStockPriceToday = dataForToday['4. close']
        lastClosingStockPrice = dataForYesterday['4. close']
        valuesChange = (float(closingStockPriceToday) - float(lastClosingStockPrice))
        percentageChange = ((valuesChange/float(lastClosingStockPrice)) * 100)

        #display +/- based on stock value changes
        if(valuesChange < 0):
            valuesChange = round(valuesChange,2)
            percentageChange = "(" + str(round(percentageChange,3)) + "%)"
        else:
            valuesChange = "+" + str(round(valuesChange,2))
            percentageChange = "(+" + str(round(percentageChange,3)) + "%)"

    return render(request, "home.html", {
        "stock_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stock_name": get_symbol(stock_symbol.upper()),
        "closingStockPriceToday": str(round(float(closingStockPriceToday),2)),
        "valuesChange": valuesChange,
        "percentageChange": percentageChange
        })
