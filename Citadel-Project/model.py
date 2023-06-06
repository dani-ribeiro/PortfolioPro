import requests
apikey = 'D9ytM36GzrbaRllf8C8dN7BCgidRY3RfkBnjNJ2w'
def port_calculation(ticker_list, shares_list):
    zipped_lists = zip(ticker_list, shares_list)
    for pair, i in enumerate(zipped_lists):
        ticker, share = pair
        requests.get(f"https://api.stockdata.org/v1/data/quote?symbols={ticker}")


def cardCreation(l1, l2) -> dict:
    # l1: list of tickers
    # l2: list of # of shares for each ticker (corresponds by index)
    # returns: dictionary. key: (str) ticker, value: (dict) data for the ticker from the api
    apikey = 'D9ytM36GzrbaRllf8C8dN7BCgidRY3RfkBnjNJ2w'
    l3 = {}
    for ticker in l1:
        val = requests.get("https://api.stockdata.org/v1/data/quote?symbols=" + ticker + "&api_token=" + apikey).json()
        l3[ticker] = val['data'][0]    
        
    return l3
 


def parser(input_str):
    return input_str.split(' ')