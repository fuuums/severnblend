#run this before market open each day
import earningsList as el
import json, csv
import requests
from HTMLParser import HTMLParser
import datetime 
import calendar
#from yahoo_finance import Share
import time

iden = []

def getTwats(ticker):
    url  = 'https://api.stocktwits.com/api/2/streams/symbol/' + ticker + '.json'
    data = json.loads(requests.get(url).text)
    twts = {}
    
    #assuming that id is unique for each tweet, and not user....
    
    for n in data["messages"]:
        if n["id"] not in iden:
            iden.append(n["id"])
            twts[n["body"]] = 0

    return twts
        
if __name__ == "__main__":
    today = ""
    tomo  = ""

    if datetime.date.today().weekday() == 3:
        today  = el.makeNasdaqUrl()
        stocks = el.getDaysEarningsNasdaq(today, True)
    else:
        today, tomo = el.makeNasdaqUrl()
        stocks = el.getDaysEarningsNasdaq(today, True) + el.getDaysEarningsNasdaq(tomo, False)
       
    while(1):
        for stock in stocks:
            twts = getTwats(stock)
            for x in twts:
                print x
        time.sleep(360) #waits for 5 minutes

    '''
    for stock in stocks:
        twts, iden = get_twats(stock, iden)
    '''
