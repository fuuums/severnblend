#run this before market open each day

import json, csv
import requests
from HTMLParser import HTMLParser
import datetime 
import calendar
from yahoo_finance import Share

def make_url():
    day    = datetime.date.today()
    sun    = day - datetime.timedelta(((day.weekday() + 1) % 7))
    sat    = day - datetime.timedelta(((day.weekday() + 1) % 7) - 6)
    day    = str(day)
    sun    = str(sun)
    sat    = str(sat)
    date   =  str(datetime.date.today() + datetime.timedelta(1))
    base   = "https://finance.yahoo.com/calendar/earnings"
    today  = base + "?from=" + sun[:4] + "-" + sun[5:7] + "-" + sun[8:] + "&to=" + sat[:4] + "-" + sat[5:7] + "-" + sat[8:] + "&day=" + day[:4] + "-" + day[5:7] + "-" + day[8:]
    tomo   = today[:78] + date[:4] + "-" + date[5:7] + "-" + date[8:]
    return (today, tomo)

def get_twats(ticker):
    url  = 'https://api.stocktwits.com/api/2/streams/symbol/' + ticker + '.json'
    data = json.loads(requests.get(url).text)

    for n in data["messages"]:
        print n["body"]
        print "\n"

class YahooHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.recording = 0
    self.data = []

  def handle_starttag(self, tag, attributes):
    if tag != 'table':
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'class' and value == 'data-table W(100%) Bdcl(c) Pos(r) BdB Bdc($c-fuji-grey-c)':
        break
    else:
      return
    self.recording = 1

  def handle_endtag(self, tag):
    if tag == 'table' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording:
      self.data.append(data)

def get_days_earnings_yahoo(url, amc):
    data   = requests.get(url).text
    parser = YahooHTMLParser()
    parser.feed(data)
    data   = parser.data
    ret    = []
    c      = 0
    
    for x in data:
        if x[0] == " ":
            continue
        if c % 6 == 0:
            ret.append(x)
        if amc and c % 6 == 2 and x == "Before Market Open":
            del ret[-1]
        elif not amc and c % 6 == 2 and x == "After Market Close":
            del ret[-1]
        elif x == "Time Not Supplied": #yahoo also gives specific times
            del ret[-1]

        c = c + 1

    return ret[1:]
    
        
if __name__ == "__main__":
    today, tomo = make_url()

    stocks = get_days_earnings_yahoo(today, True) + get_days_earnings_yahoo(tomo, False)
    for stock in stocks:
        print stock

    '''
    for stock in stocks:
        get_twats(stock)
    '''
