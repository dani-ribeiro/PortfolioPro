import requests

apikey = '<INSERT_NEW_API_KEY>'

def getStocks(ticker):
    if ticker == "NONE" or ticker == "None" or ticker == "":
        return None
    ticker_stock = dict(requests.get(f"https://api.stockdata.org/v1/data/quote?symbols={ticker}&api_token={apikey}").json())
    return ticker_stock

def clean_up(ticker_list, shares_list):
    new_ticker_list = []
    new_shares_list = []
    for i, ticker in enumerate(ticker_list):
        if not(ticker in ["NONE", "none", "None", ""]):
            if ticker in new_ticker_list:
                ix = new_ticker_list.index(ticker)
                new_shares_list[ix] += shares_list[i]
            else: 
                new_ticker_list.append(ticker)
                new_shares_list.append(int(shares_list[i]))
    return new_ticker_list, new_shares_list

def port_calculation(ticker_list, shares_list, price_list) -> list:
    ticker_list, shares_list = clean_up(ticker_list, shares_list)
    zipped_lists = zip(ticker_list, shares_list, price_list)
    total = 0
    for _, triplet in enumerate(zipped_lists):
        _, share, price = triplet
        total += price*share

    
    return [(ticker_list[i], round(shares_list[i]*price*100/total, 2)) for i, price in enumerate(price_list)]



def cardCreation(ticker_list, shares_list) -> dict:
    # l1: list of tickers
    # l2: list of # of shares for each ticker (corresponds by index)
    # returns: dictionary. key: (str) ticker, value: (dict) data for the ticker from the api
    data_list = {}
    price_list = []
    ticker_list, shares_list = clean_up(ticker_list, shares_list)
    total_val = 0 
    
    for i, ticker in enumerate(ticker_list):
        ticker_data = getStocks(ticker)['data'][0]
        # ticker_data['percent'] = percent_list[i]
        ticker_data['shares'] = shares_list[i]
        data_list[ticker] = ticker_data
        price = ticker_data['price']
        price_list.append(price)
        total_val += shares_list[i]*price
    percent_list = port_calculation(ticker_list, shares_list, price_list)
    
    for i, ticker in enumerate(ticker_list):
        data_list[ticker]['percent'] = percent_list[i]
    return data_list, total_val

def add_shares(ticker_list, shares_list, ticker, add_shares):
    ix = ticker_list.index(ticker)
    shares_list[ix] += add_shares
    return ticker_list, shares_list
      
def remove_shares(ticker_list, shares_list, ticker, remove_shares = "All"):
    ix = ticker_list.index(ticker)
    if remove_shares == "All" or remove_shares >= shares_list[ix]:
        ticker_list.pop(ix)
        shares_list.pop(ix)
    else: 
        shares_list[ix] = shares_list[ix] - remove_shares
    return ticker_list, shares_list

def sorted_percent_list(data_list):
    return sorted([(ticker, ticker['percent']) for ticker in data_list], key = lambda x: x[1])[::-1]
