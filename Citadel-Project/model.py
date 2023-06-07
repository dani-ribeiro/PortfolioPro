import requests

apikey = 'D9ytM36GzrbaRllf8C8dN7BCgidRY3RfkBnjNJ2w'

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
    zipped_lists = zip(ticker_list, shares_list, price_list) # error
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

# def update_data_list(data_list, ticker_list, shares_list):
#     ticker_list, shares_list = clean_up(ticker_list, shares_list)
#     total_val = 0
#     for i, ticker in enumerate(ticker_list):
#         if ticker in data_list:
#             data_list[ticker]['shares'] += shares_list[i] #add the new shares
#         else: 
#             ticker_data = getStocks(ticker)['data'][0] #get the data for the stock
#             ticker_data['shares'] = shares_list[i] #add the value of the stocks
#             data_list[ticker] = ticker_data #add the new data

#         price = data_list[ticker]['price']
#         total_val += price*data_list[ticker]['shares'] #add price*shares to the total value
#     for ticker in data_list:
#         price = data_list[ticker]['price']
#         ticker_val = price*data_list[ticker]['shares']
#         data_list[ticker]['percent'] = round(ticker_val*100/total_val, 2) #get the percentages
#     return data_list, total_val
        
def remove_data_list(data_list, ticker_list, shares_list):
    ticker_list, shares_list = clean_up(ticker_list, shares_list)
    total_val = 0
    for i, ticker in enumerate(ticker_list):
        if ticker in data_list:
            data_list[ticker]['shares'] -= shares_list[i] #add the new shares
            if data_list[ticker]['shares'] <= 0: 
                del data_list[ticker]
            else: total_val += data_list[ticker]['price'] * data_list[ticker]['shares']
        else: continue
        
    for ticker in data_list:
        price = data_list[ticker]['price']
        ticker_val = price*data_list[ticker]['shares']
        data_list[ticker]['percent'] = round(ticker_val*100/total_val, 2) #get the percentages
    return data_list, total_val
        


def give_percent_list(data_list):
    return [(ticker, ticker['percent']) for ticker in data_list]
