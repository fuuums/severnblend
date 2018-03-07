#run this before market open each day
import earningsList as el
import json, csv
import requests
from HTMLParser import HTMLParser
import datetime
import calendar
import pymysql
#from yahoo_finance import Share
import time
import schedule

iden = []

minCap = 25
maxCap = 1000



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

def autoCollect():
    today = ""
    tomo  = ""
    loop =True
    count = 0
    if datetime.date.today().weekday() == 3:
        today  = el.makeNasdaqUrl()
        stocks = el.getDaysEarningsNasdaq(today, True, minCap, maxCap)
    else:
        today, tomo = el.makeNasdaqUrl()
        stocks = el.getDaysEarningsNasdaq(today, True, minCap, maxCap) + el.getDaysEarningsNasdaq(tomo, False, minCap, maxCap)

    # Create the connection to the Database
    conn = pymysql.connect(host='midn.cs.usna.edu', port=3306, user='earnings', passwd='severnblend', db='capstone-earnings', charset='utf8')
    cur = conn.cursor()
    while(count < 120):
        print "Size " + str(len(stocks))
        if len(stocks) == 0:
            print "None to poll!"
            loop = False
            break
        for stock in stocks:
            twts = getTwats(stock[0])
            for x in twts:
                # Write the tweets to the database
                try:
                    print x
                    cur.execute("""INSERT INTO testRawFeed (tweet) values (%s)""", (x))
                    conn.commit()
                except UnicodeEncodeError:
                    pass
            time.sleep(25) #waits for 25 seconds
            count = count + 1
            # Only get 200 requests per hour, with 30 tweets per request
    # Close the connection
    cur.close()
    conn.close()
    # Cancel the running job
    return schedule.CancelJob
def clearTables():
    conn = pymysql.connect(host='midn.cs.usna.edu', port=3306, user='earnings', passwd='severnblend', db='capstone-earnings', charset='utf8')
    cur = conn.cursor()
    cur.execute("""TRUNCATE TABLE testRawFeed""")
    conn.commit()
    # Close the connection
    cur.close()
    conn.close()
    # Cancel the running job
    return schedule.CancelJob


# Setting up the automatic running of this program
## Note the time
# Clear out the old tweets
schedule.every().day.at("16:00").do(clearTables)
schedule.every().hour.do(autoCollect)



while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
