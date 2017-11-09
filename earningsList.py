# Fetches list of companies reporting earnings
# Not to be used on Fridays

import json, csv
import requests
from HTMLParser import HTMLParser
import datetime 
import calendar
from yahoo_finance import Share

def makeNasdaqUrl():
    day    = datetime.date.today()
    tomo   = datetime.date.today() + datetime.timedelta(days=1)
    n      = day.weekday()
    day    = str(day)
    tomo   = str(tomo)
    base   = "http://www.nasdaq.com/earnings/earnings-calendar.aspx?date="
    today  = base + day[:4] + "-" + day[5:7] + "-" + day[8:]
    next   = ""
    if n == 3:
        return today
    else:
        return (today, base + tomo[:4] + "-" + tomo[5:7] + "-" + tomo[8:])
    

class NasdaqHTMLParser(HTMLParser):
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
      if name == 'class' and value == 'USMN_EarningsCalendar':
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

def getDaysEarningsNasdaq(url, amc):
    data   = requests.get(url).text
    parser = NasdaqHTMLParser()
    parser.feed(data)
    data   = parser.data
    d      = 0
    cn     = 0
    mc     = 0
    l      = []
    ticker = ""
    c      = 0
    
    for x in data:
        x = x.strip()
        if x != "" and x[0].isupper():
            if cn == 1 and x == "Company Name (Symbol)":
                break
            if x == "Company Name (Symbol)":
                cn = 1
            if mc == 1 and x[:11] == "Market Cap:":
                mc = 0
                if x[-1] == "a" or x[-1] == "M":
                    continue
                else:
                    marketCap = x.split("$", 1)[1]
                    marketCap = marketCap[:-1]
                    marketCap = float(marketCap)
                    if marketCap > 25:
                        l.append(ticker)
            if d == 1 and x[-1] == ")":
                d = 0
                mc = 1
                ticker = x[x.find("(")+1:x.find(")")]
            if x == "Met":
                d = 1
    return l

if __name__ == "__main__":
    today = ""
    tomo  = ""

    if datetime.date.today().weekday() == 3:
        today  = makeNasdaqUrl()
        stocks = getDaysEarningsNasdaq(today, True)
    else:
        today, tomo = makeNasdaqUrl()
        stocks = getDaysEarningsNasdaq(today, True) + getDaysEarningsNasdaq(tomo, False)

    for stock in stocks:
        print stock
