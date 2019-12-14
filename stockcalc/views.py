import requests
import datetime
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(
        symbol)
    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


def input_map(input):
    stockMap = {
        "Ethical Investing": ["AAPL", "ADBE", "NSRGY"],
        "Growth Investing": ["FB", "NVDA", "CRM"],
        "Index Investing": ["VTI", "IXUS", "ILTB"],
        "Quality Investing": ["UTX", "NOW", "PYPL"],
        "Value Investing": ["GD", "KMX", "VLO"]
    }

    if(input in stockMap and input != None):
        return stockMap[input]


def compute_stock(input):

    for i in input:
        strategy1MapStocks = requests.get(
            'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + i + '&apikey=R2CDNLQSS8YOEHZU')
        strategyStockData = strategy1MapStocks.json()['Time Series (Daily)']
        currentClosing = strategyStockData[list(
            strategyStockData)[0]]['4. close']
        previousClosing = strategyStockData[list(
            strategyStockData)[1]]['4. close']
        print(i + "(current closing): $" + currentClosing)
        print(i + "(previous closing): $" + previousClosing)


def fetch_stock(request):

    # input maps to investment strategies -> ETFs/Stocks
    stock_symbol = request.GET['tickerSymbol']
    strategy1Map = input_map(request.GET['strategy1'])
    strategy2Map = input_map(request.GET.get('strategy2', None))
    print(strategy1Map)
    print(strategy2Map)

    # iterate through first strategy map and call apis 3 times
    compute_stock(strategy1Map)

    #----------------------------------------------------------------------------------------------------------------------#
    # uses alphavantage stock api to fetch latest stock data in time series
    getStock = requests.get(
        'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_symbol + '&apikey=R2CDNLQSS8YOEHZU')

    if (getStock.status_code == 200):
        # fetch stock data in JSON and then get current and previous closing data
        stockData = getStock.json()['Time Series (Daily)']
        # compute differences between current & previous closing stock prices
        closingStockPriceToday = stockData[list(stockData)[0]]['4. close']
        lastClosingStockPrice = stockData[list(stockData)[1]]['4. close']
        valuesChange = (float(closingStockPriceToday) -
                        float(lastClosingStockPrice))
        percentageChange = ((valuesChange/float(lastClosingStockPrice)) * 100)

        # display +/- based on stock value changes
        if(valuesChange < 0):
            valuesChange = round(valuesChange, 2)
            percentageChange = "(" + str(round(percentageChange, 3)) + "%)"
        else:
            valuesChange = "+" + str(round(valuesChange, 2))
            percentageChange = "(+" + str(round(percentageChange, 3)) + "%)"

    return render(request, "home.html", {
        "stock_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stock_name": get_symbol(stock_symbol.upper()),
        "closingStockPriceToday": str(round(float(closingStockPriceToday), 2)),
        "valuesChange": valuesChange,
        "percentageChange": percentageChange,
        "strategy1": request.GET['strategy1'], "strategy1Map": strategy1Map,
        "strategy2": request.GET.get('strategy2', None), "strategy2Map": strategy2Map
    })
