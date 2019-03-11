import urllib.request, time
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool


headers = ['Date', 'Open', 'High','Low','Close','Adj Close', 'Vol']



urls = [    "https://finance.yahoo.com/quote/MSFT/history?p=MSFT",
            "https://finance.yahoo.com/quote/XOM/history?p=XOM",
            "https://finance.yahoo.com/quote/JNJ/history?p=JNJ",
            "https://finance.yahoo.com/quote/GE/history?p=GE",
            "https://finance.yahoo.com/quote/FB/history?p=FB",
            "https://finance.yahoo.com/quote/AMZN/history?p=AMZN",
            "https://finance.yahoo.com/quote/BRK-B/history?p=BRK-B",
            "https://finance.yahoo.com/quote/T/history?p=T",
            "https://finance.yahoo.com/quote/WFC/history?p=WFC"
            ]

class Scrape:
    def __init__(self, thickers={}):
        self.thickers = thickers

    def getName(self, name=[]):
        self.thickers = name
        

    def getURL(self, x=0, pool=ThreadPool(32)):
        print(self.thickers)
        try:
            res = pool.map(urllib.request.urlopen, urls)
        except urllib.error.HTTPError as e:
            print('HTTP ERR: {}'.format(e.code)) 
        except urllib.error.URLError as e:
            print('URLError: {}'.format(e.reason))
        else:
            while x < len(urls):
                print('Status code : ' , res[x].getcode(), "\t", urls[x]) 
                self.getContent(res[x])              
                pool.close()
                pool.join()   
                res[x].close()
                x += 1

            
    data = []
    def getContent(self, res):
        bytesStrdata = res.read()
        strNew = bytesStrdata.decode('utf-8')
        raw = BeautifulSoup(strNew, 'html.parser')
        tableBody = raw.find_all('table', attrs={'class': 'W(100%) M(0)'})
        table_body = tableBody[0].find('tbody')
        rows = table_body.find_all('tr')
        for i in range(0,len(rows)):
            cols = [ele.text.strip() for ele in rows[i].find_all('td')]
            self.data.append(cols)
        self.frameObjects(self.data)    
            
    def frameObjects(self, obj):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            dataFrame = pd.DataFrame(obj, columns=headers)
            return (dataFrame)
            
            



    

