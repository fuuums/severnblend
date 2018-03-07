# Fetches list of companies reporting earnings
# Not to be used on Fridays

import json, csv
import requests
from HTMLParser import HTMLParser
import datetime
import calendar
import sys
import pymysql
#from yahoo_finance import Share

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

# Add feature for the minimum and max marketCap values by user factored in
def getDaysEarningsNasdaq(url, amc, minCap, maxCap):
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
                    # Check to see if the ticker is in range of the user defined min and max
                    if marketCap >= minCap and marketCap <= maxCap:
                        # Check to see ticker length accurate
                        if len(ticker) <= 4:
                            l.append((ticker, int(marketCap)))
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

    # Handle the user entered minCap and maxCap values as element of command line arguments
    # First Argument: minCap
    # Second Argument: maxCap
    # Doesn't take into account companies with a marketCap below $1 billion even if they're reporting, too small to care about
    # Default action if no minCap and maxCap is minCap of $25 billion and $1000 billion, or $1 twillion
    goodInput = True
    minCap = 25
    maxCap = 1000
    # Check for user input, if no values given or more than the minCap and maxCap then simply uses default values
    if len(sys.argv) != 3:
        minCap = 25
        maxCap = 1000
    else:
        # Check that the args are all digits
        for arg in sys.argv[1:]:
            if arg.isdigit():
                goodInput = True
            else:
                goodInput = False
                break;
        # Had all good digit inputs so now update the minCap and maxCap values
        if goodInput:
            # Ensuring larger number is max and lower is the minCap
            if int(sys.argv[1]) >= int(sys.argv[2]):
                minCap = int(sys.argv[2])
                maxCap = int(sys.argv[1])
            else:
                minCap = int(sys.argv[1])
                maxCap = int(sys.argv[2])


    if datetime.date.today().weekday() == 3:
        today  = makeNasdaqUrl()
        stocks = getDaysEarningsNasdaq(today, True, minCap, maxCap)
    else:
        today, tomo = makeNasdaqUrl()
        stocks = getDaysEarningsNasdaq(today, True, minCap, maxCap) + getDaysEarningsNasdaq(tomo, False, minCap, maxCap)

    # Handle the weird issue of having the string "The" as a stock
    stocks = [i for i in stocks if i[0] != "The"]

    # Set up the connection to the database
    #Database connection
    conn = pymysql.connect(host='midn.cs.usna.edu', port=3306, user='earnings', passwd='severnblend', db='capstone-earnings', charset='utf8')
    cur = conn.cursor()
    # Clear out the table that has the stocks reporting that day
    cur.execute("TRUNCATE TABLE reportingCompaniesTickers")
    # Enter in the new tickers for companies reporting that day
    for stock in stocks:
        print str(stock[0])
        cur.execute("""INSERT INTO reportingCompaniesTickers (ticker, marketCap) values (%s, %s)""", (stock[0], stock[1]))
    # Close the connection
    conn.commit()
    cur.close()
    conn.close()
