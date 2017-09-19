import json, csv
import requests
from HTMLParser import HTMLParser
import datetime
import calendar
from yahoo_finance import Share

def get_twats(ticker):
    url  = 'https://api.stocktwits.com/api/2/streams/symbol/' + ticker + '.json'
    data = json.loads(requests.get(url).text)

    for n in data["messages"]:
        print n["body"]
        print "\n"

class MyHTMLParser(HTMLParser):
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

        
def get_days_earnings(url):
    data   = requests.get(url).text
    parser = MyHTMLParser()
    parser.feed(data)
    data   = parser.data
    ret    = []

    r = False
    for x in data:
        x = x.strip(' \t\n\r')
        if x == "Company Name (Symbol)" and r == True:
            break
        elif x == "Company Name (Symbol)" and r == False:
            r = True

        if x.endswith(')') and x != "Company Name (Symbol)":
            ret.append(x[x.index("(") + 1:x.rindex(")")])

    return ret
        
if __name__ == "__main__":
    date   =  str(datetime.date.today() + datetime.timedelta(1))
    year   = date[:4]
    month  = date[5:7]
    date   = date[8:10]
    today  = "http://www.nasdaq.com/earnings/earnings-calendar.aspx"
    tomo   =  today + "?date=" + year +  "-" + month + "-" + date
    stocks = get_days_earnings(today) + get_days_earnings(tomo)

    
    for stock in stocks:
        print stock
