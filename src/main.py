
'''
Auhtor : Sadik Erisen

'''

import os
import requests
from requests.exceptions import Timeout
import time, datetime
import json
import aiohttp
import asyncio
import six
from typing import Callable, List, Any
from abc import ABCMeta


from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


ENDPOINTS = [
    "https://query1.finance.yahoo.com/v8/finance/chart/",
    "http://www.barchart.com/stocks/sp500.php"

]




class AbstractComsumer(object):
    class handleError(Exception):
        pass
    
    def __init__(self):
        self.dataframe = None

    def url_RESPONSE(self, url): 
        FLAG = False
        counter = 0
        raw = None

        while not FLAG:
            try:
                raw = requests.get(url)
                FLAG = True
            except (requests.HTTPError, requests.ConnectionError) as e:
                if counter < 3:
                   counter += 1
                   waitfor = 5 ** counter
                   time.sleep(waitfor)
                else:
                    raise (e)
        return  raw         

    def get_DATAFRAME(self):
        return self.dataframe

    def HandleDate(self, date):
        ConvertedDate = datetime.datetime.utcfromtimestamp(date)
        x = ConvertedDate[0]
        print(x)
        # constructDate = ConvertedDate.date()
        # date = constructDate.strftime("%Y-%m-%d")
        # return date

    def HandleTime(self, t):
        ConvertedTime = datetime.datetime.utcfromtimestamp(t)
        constructTime = ConvertedTime.time()
        newTime = constructTime.strftime("%H:%M")
        return newTime

    def write_ToCSV(self, path='output.csv'):
        if not path[-4:] == '.csv':
            path += '.csv'     
        self.dataframe.to_csv(path, index=True)


class BarChart_SNP500(AbstractComsumer):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def reponseContent(self):
        result = self.url_RESPONSE(self.url)
        raw = BeautifulSoup(result, 'html.parser')
        return raw

    def ExtractData(self, data=[]):
        raw = self.reponseContent()
        tables = raw.find_all('table', attrs={'class': 'W(100%) M(0)'})
        table_body = tables[0].find('tbody')
        rows = table_body.find_all('tr')

        for i in range(0, len(rows)):
            cols = [ele.text.strip() for ele in rows[i].find_all('td')]
            data.insert(i, cols)
        print(data[0])





class YahooFinance(AbstractComsumer):

    def __init__(self, symbol, duration, interval):
        super().__init__()
        self.url = ENDPOINTS[0]
        self.symbol = symbol
        self.duration = duration
        self.interval = interval

    def create_URL(self):
        ''' 
        $symbol is the stock ticker symbol, e.g. AAPL for Apple
        $range/duration is the desired range of the query, allowed parameters are [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]
        $interval is the desired interval of the quote, e.g. every 5 minutes, allowed parameters are [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3m
        '''
        url = ('%s?range=%s&interval=%s' %
               (self.symbol, self.duration, self.interval))
        query = self.url + url
        return query


    def reponseContent(self):
        result = self.url_RESPONSE(self.create_URL())
        data = result.json()
        return data

    def CompanyMetaData(self):
        raw =  self.reponseContent()
        CompanyMetaData = raw['chart']['result'][0]['meta']
        return CompanyMetaData


    
    def CompanyNameQuote(self):    
        raw = self.reponseContent()
        
        CompanyQuotes=[]

        CompnayTicker = raw['chart']['result'][0]['meta']['symbol']
        Date = raw['chart']['result'][0]['timestamp'][0]
        newDate = self.HandleDate(Date)
        newTime = self.HandleTime(Date)
        High = raw['chart']['result'][0]['indicators']['quote'][0]['high'][0]
        Low = raw['chart']['result'][0]['indicators']['quote'][0]['low'][0]
        Open = raw['chart']['result'][0]['indicators']['quote'][0]['open'][0]
        Close = raw['chart']['result'][0]['indicators']['quote'][0]['close'][0]
        Adj_Close = raw['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
        Volume = raw['chart']['result'][0]['indicators']['quote'][0]['volume'][0]
        CompanyQuotes.append((
            CompnayTicker, 
            newDate,
            newTime,
            High, Low,
            Open, 
            Close,
            Adj_Close,
            Volume))

        return CompanyQuotes[0]
        
    
        


ytd = YahooFinance('AAPL', '1d', '1d')
x = ytd.CompanyNameQuote()
print(x)





















# class NameOBJECTS(object):
    
#     def __init__(self, raw):
#         self.raw = raw

#     def getNames(self):    
#         tableBody = self.raw.findAll('a', attrs={"data-component": "link"})  
#         data = [i.text for i in tableBody]
#         return data
        

# class UrlOBJECTS(object):

#     def __init__(self, baseURL):
#         self.baseURL = baseURL

#     def createURLs(self, name=[]):
#         urls = [self.baseURL + i +"/history?p="+i for i in name]
#         return urls
        

# class CompanyDirectories(object):
#     def __init__(self, names):
#         self.names = names

#     def createDirectory(self):

#         if (gb.os.path.exists(gb.PATH)):
#             for dr in self.names:
#                 absPATH = gb.PATH + dr
#                 gb.os.mkdir(absPATH)
#                 open(absPATH + "/" + dr + ".json", "w+")
#         else:
#             print (
#                 "The directory of %s does not exist ... now creating the directory" % gb.PATH)
#             try:
#                 gb.os.makedirs(gb.PATH)
#                 for dr in self.names:
#                     absPATH = gb.PATH + dr
#                     gb.os.mkdir(absPATH)
#                     open(absPATH + "/" + dr + ".json", "w+")
#             except OSError:
#                 print(
#                     'failed to create the directory ... please re-run the routine again ...')
#             else:
#                 print("Successfully created the directory of %s" %
#                       gb.PATH)
#                 self.createDirectory()
                


# scrp_name = ScrapeData(gb.ENDPOINTS[1])
# __NAMES = NameOBJECTS(scrp_name.reponseContent())
# __URL = UrlOBJECTS(gb.ENDPOINTS[0])
# tags = __NAMES.getNames()

# @gb.asyncio.coroutine
# async def CreateDic():
#     __DIR =  CompanyDirectories(tags)
#     create__ =  __DIR.createDirectory()
#     return create__
 

# @gb.asyncio.coroutine
# async def CreateURL():
#     create_url = __URL.createURLs(tags)
#     return create_url


# class HistoricData:

#     @classmethod
#     async def call_List(cls, url):
#         data = []
#         response = await gb.aiohttp.ClientSession().get(url)
#         bytesStrdata = await response.read()
#         strNew = bytesStrdata.decode('utf-8')
#         raw = gb.BeautifulSoup(strNew, 'html.parser')
#         tables = raw.find_all('table', attrs={'class': 'W(100%) M(0)'})
#         table_body = tables[0].find('tbody')
#         rows = table_body.find_all('tr')

#         for i in range(0, len(rows)):
#             cols = [ele.text.strip()
#             for ele in rows[i].find_all('td')]
#             data.insert(i, cols)
        
#         with gb.pd.option_context('display.max_rows', 200, 'display.max_columns', 200):
#             dataFrame = gb.pd.DataFrame(data, columns=gb.HEADERS).to_json()
#             print(dataFrame)
        
#         for tag in tags:
#             newPath = gb.PATH + tag + "/" + tag + ".json"
#             f = open(newPath, 'w')
#             f.write(dataFrame)
#             print('done...')
#             f.close()

#         return data

    

#     @classmethod
#     async def execute(cls):
#         urls = await CreateURL()
#         futures = [HistoricData.call_List(url) for url in urls]
#         await gb.asyncio.wait(futures)


# async def main():
#     if not (gb.os.path.exists("Companies/")):
#         await gb.asyncio.gather(CreateDic(), HistoricData.execute(), CreateURL())
#     else:
#         gb.os.system("clear")
#         print('files exist...')
#         # HistoricData.ddff("")
#         await gb.asyncio.gather(HistoricData.execute(), CreateURL())
        


# if __name__ == "__main__":
#     loop = gb.asyncio.get_event_loop()
#     loop.run_until_complete(main())
 
