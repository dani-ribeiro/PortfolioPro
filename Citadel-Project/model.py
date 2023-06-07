import requests

apikey = 'D9ytM36GzrbaRllf8C8dN7BCgidRY3RfkBnjNJ2w'

def getStocks(ticker):
    if ticker == "NONE" or ticker == "None" or ticker == "":
        return None
    ticker_stock = dict(requests.get(f"https://api.stockdata.org/v1/data/quote?symbols={ticker}&api_token={apikey}").json())
    return ticker_stock

def remove_none(ticker_list, shares_list):
    new_ticker_list = []
    new_shares_list = []
    for i, ticker in enumerate(ticker_list):
        if not(ticker == "NONE" or ticker == "None" or ticker == ""):
            new_ticker_list.append(ticker)
            new_shares_list.append(shares_list[i])
    return new_ticker_list, new_shares_list

def port_calculation(ticker_list, shares_list, price_list) -> list:
    ticker_list, shares_list = remove_none(ticker_list, shares_list)
    zipped_lists = zip(ticker_list, shares_list, price_list) # error
    total = 0
    for _, triplet in enumerate(zipped_lists):
        _, share, price = triplet
        total += price*int(share)

    
    return [(ticker_list[i], round(int(shares_list[i])*price*100/total, 2)) for i, price in enumerate(price_list)]



def cardCreation(ticker_list, shares_list) -> dict:
    # l1: list of tickers
    # l2: list of # of shares for each ticker (corresponds by index)
    # returns: dictionary. key: (str) ticker, value: (dict) data for the ticker from the api
    data_list = {}
    price_list = []
    ticker_list, shares_list = remove_none(ticker_list, shares_list)
    
    for i, ticker in enumerate(ticker_list):
        ticker_data = getStocks(ticker)['data'][0]
        # ticker_data['percent'] = percent_list[i]
        ticker_data['shares'] = shares_list[i]
        data_list[ticker] = ticker_data
        price_list.append(ticker_data['price'])
    percent_list = port_calculation(ticker_list, shares_list, price_list)
    for i, ticker in enumerate(ticker_list):
        data_list[ticker]['percent'] = percent_list[i]
    
    return data_list

def pie_percent_calculation(data_list):
    percent_list = []
    for ticker in data_list:
        percent_list.append((ticker, ticker['percent']))
    return percent_list
