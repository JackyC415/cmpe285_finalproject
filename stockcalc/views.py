import requests
import datetime
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


def get_symbol(symbol):

    # convert abbreviated stock symbol to actual company name
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(
        symbol)
    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


def input_map(input):

    # dictionary that maps investment strategies to stocks/etfs
    stockMap = {
        "Ethical Investing": ["AAPL", "ADBE", "NSRGY"],
        "Growth Investing": ["FB", "NVDA", "CRM"],
        "Index Investing": ["VTI", "IXUS", "ILTB"],
        "Quality Investing": ["UTX", "NOW", "PYPL"],
        "Value Investing": ["GD", "KMX", "VLO"]
    }

    if(input in stockMap and input != None):
        return stockMap[input]


def compute_stock(stocks, investment):

    stock_list, history_list = [], []
    for stock_name in stocks:
        # uses alphavantage stock API to fetch latest stock data in time series
        strategyMapStocks = requests.get(
            'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock_name+'&apikey=R2CDNLQSS8YOEHZU')

        if (strategyMapStocks.status_code == 200):
            # fetch stock data in JSON and then get current and previous closing data
            strategyStockData = strategyMapStocks.json()['Time Series (Daily)']
            currentClosing = strategyStockData[list(
                strategyStockData)[0]]['4. close']
            previousClosing = strategyStockData[list(
                strategyStockData)[1]]['4. close']
            # compute differences between current & previous closing stock prices to determine values change
            valuesChange = (float(currentClosing) - float(previousClosing))
            percentageChange = ((valuesChange/float(previousClosing)) * 100)
            closingDate = list(strategyStockData)[0]

            # display +/- based on stock value changes
            if(valuesChange < 0):
                valuesChange = round(valuesChange, 2)
                percentageChange = "(" + str(round(percentageChange, 3)) + "%)"
            else:
                valuesChange = "+" + str(round(valuesChange, 2))
                percentageChange = "(+" + \
                    str(round(percentageChange, 3)) + "%)"

        # store computed stock data in a list to return for rendering
        stock_list.append("Company: {} Closing Date: {} Stock: {} {} {} Investment: ${:.2f}".format(
            get_symbol(stock_name),
            closingDate,
            currentClosing,
            valuesChange,
            percentageChange,
            (int(investment)/len(stocks))
        ))

        # fetch previous 5 days of stock history for each stock
        for stock_date in list(strategyStockData)[0:5]:
            history_list.append("Company: {} Closing Date: {} Stock: {} ".format(
                get_symbol(stock_name),
                stock_date,
                strategyStockData[stock_date]
            ))

    return stock_list, history_list


def fetch_stock(request):

    # input maps to investment strategies -> ETFs/Stocks
    investAmount = request.GET['investAmount']
    strategy1Map = input_map(request.GET['strategy1'])
    strategy2Map = input_map(request.GET.get('strategy2', None))

    # ensure investment amount is greater than 5000
    if(int(investAmount) < 5000):
        print('Minimum investment is $5000')
    else:
        # compute first investment strategy
        stock_list, history_list = compute_stock(strategy1Map, investAmount)
        # since second investment strategy is optional, check for null
        if(strategy2Map != None):
            compute_stock(strategy2Map, investAmount)

    print(type(request.GET.get('strategy2', None)))
    return render(request, "home.html", {
        "strategy1": request.GET['strategy1'], "strategy1Map": strategy1Map,
        "strategy2": request.GET.get('strategy2', None), "strategy2Map": strategy2Map,
        "stock_list": stock_list,
        "stock_history": history_list
    })
