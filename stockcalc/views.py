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

    stock_list, history_list, imagelist = [], [], []
    for stock_name in stocks:
        # uses alphavantage stock API to fetch latest stock data in time series
        strategyMapStocks = requests.get(
            'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock_name+'&apikey=WW1TTWRBNMVWNH9G')
        imagelist.append(showChart(strategyMapStocks.json()))

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

    return stock_list, history_list, imagelist


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
        stock_list, history_list, imagelist  = compute_stock(strategy1Map, investAmount)
        # since second investment strategy is optional, check for null
        if(strategy2Map != None):
            compute_stock(strategy2Map, investAmount)

    print(type(request.GET.get('strategy2', None)))
    return render(request, "home.html", {
        "strategy1": request.GET['strategy1'], "strategy1Map": strategy1Map,
        "strategy2": request.GET.get('strategy2', None), "strategy2Map": strategy2Map,
        "stock_list": stock_list,
        "stock_history": history_list,
        'images': imagelist
    })


def showChart(json):
    import pandas
    import matplotlib.pyplot as plt
    from mpl_finance import candlestick_ohlc
    import matplotlib.dates as mdates
    import io
    import base64
    stockJSON = json
    df = pandas.DataFrame()
    df['Date'] = list(stockJSON['Time Series (Daily)'].keys())
    df['Date'] = pandas.to_datetime(df['Date'])
    df['Date'] = df['Date'].map(mdates.date2num)
    open = []
    close = []
    high = []
    low = []
    dataList = list(stockJSON['Time Series (Daily)'].values())
    for i in range(len(dataList)):
        open.append(float(dataList[i]['1. open']))
        high.append(float(dataList[i]['2. high']))
        low.append(float(dataList[i]['3. low']))
        close.append(float(dataList[i]['4. close']))
    df['open'] = open
    df['high'] = high
    df['low'] = low
    df['close'] = close
    ax = plt.subplot()
    candlestick_ohlc(ax, df.values, width=1, colorup='g', colordown='r')
    ax.xaxis_date()
    date_format = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.grid(True)
    ax.set_title(stockJSON['Meta Data']['2. Symbol'], color='black')
    figureBuffer = io.BytesIO()
    plt.savefig(figureBuffer, dpi=100,format='png')
    image_png = figureBuffer.getvalue()
    figureBuffer.close()
    plt.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

