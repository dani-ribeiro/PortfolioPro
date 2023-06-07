import requests

apikey = 'D9ytM36GzrbaRllf8C8dN7BCgidRY3RfkBnjNJ2w'
def port_calculation(ticker_list, shares_list) -> list:
    zipped_lists = zip(ticker_list, shares_list)
    total = 0
    price_list = []
    for _, pair in enumerate(zipped_lists):
        ticker, share = pair
        comp_data = dict(requests.get(f"https://api.stockdata.org/v1/data/quote?symbols={ticker}&api_token={apikey}").json())
        price = comp_data['data'][0]['price']
        total += price*share
        price_list.append(price)
    
    return [(ticker_list[i], round(shares_list[i]*price*100/total, 2)) for i, price in enumerate(price_list)]


    

def cardCreation(l1, l2) -> dict:
    # l1: list of tickers
    # l2: list of # of shares for each ticker (corresponds by index)
    # returns: dictionary. key: (str) ticker, value: (dict) data for the ticker from the api
    apikey = 'D9ytM36GzrbaRllf8C8dN7BCgidRY3RfkBnjNJ2w'
    l3 = {}
    for ticker in l1:
        val = dict(requests.get(f"https://api.stockdata.org/v1/data/quote?symbols={ticker}&api_token={apikey}").json())
        print(val)
        l3[ticker] = val['data'][0] # key: ticker; value: all data for the ticker from stockdata   
        
    return l3
 


def parser(input_str):
    return input_str.split(' ')