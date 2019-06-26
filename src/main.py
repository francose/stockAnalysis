
'''
Auhtor : Sadik Erisen
Version : 0.1
'''

import os, time, datetime, json ,six
from typing import Callable, List, Any
from abc import ABCMeta

import asyncio
import requests
from requests.exceptions import Timeout
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


ENDPOINTS = [
    "https://query1.finance.yahoo.com/v8/finance/chart/",
    "http://www.barchart.com/stocks/indices/sp/sp500"

]




class AbstractComsumer(object):
    class handleError(Exception):
        pass
    
    def __init__(self):
        self.dataframe = None
 
    def fetch(self, url): 
        FLAG = False
        counter = 0
        raw = None

        while not FLAG:
            try:
                raw =  requests.get(url)
                FLAG = True
            except (requests.HTTPError, requests.ConnectionError) as e:
                if counter < 3:
                   counter += 1
                   waitfor = 5 ** counter
                   time.sleep(waitfor)
                else:
                    raise (e)
        return  raw         

    def get_DATAFRAME(self, sdoc:str) -> str:
        self.dataframe = pd.DataFrame(sdoc)
        return self.dataframe

    def HandleDate(self,  d: []) -> None:
        return [str(datetime.datetime.fromtimestamp(t)) for t in d]

    def write_ToCSV(self, path='output.json'):
        if not path[-4:] == '.json':
            path += '.json'     
        self.dataframe.to_csv(path, index=True)



class YahooFinance(AbstractComsumer):

    def __init__(self, symbol:str, duration:str, interval:str)-> str:
        super().__init__()
        self.url = ENDPOINTS[0]
        self.symbol = symbol
        self.duration = duration
        self.interval = interval



    def create_URL(self, query=[]):
        ''' 
        $symbol is the stock ticker symbol, e.g. AAPL for Apple
        $range/duration is the desired range of the query, allowed parameters are [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]
        $interval is the desired interval of the quote, e.g. every 5 minutes, allowed parameters are [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3m
        ''' 
        url = ('%s?range=%s&interval=%s' %
            (self.symbol, self.duration, self.interval))
        query= self.url + url
        return query    

    def reponseContent(self):
        result = self.fetch(self.create_URL())
        data = result.json()
        return data

    def CompanyMetaData(self):
        raw =  self.reponseContent()
        dataFrame = self.get_DATAFRAME(raw)
        return dataFrame

    def CompanyQuotes(self, CompanyQuotes=[]):
        raw = self.CompanyMetaData()
        data = raw['chart']['result'][0]
        newDate = self.HandleDate(data['timestamp'])
        if "m" == self.interval[1]:
            for i in range(0, len(data['timestamp'])):
                CompanyQuotes.append(
                {
                    "date": newDate[i],
                    "high": data['indicators']['quote'][0]['high'][i],
                    "low": data['indicators']['quote'][0]['low'][i],
                    "open": data['indicators']['quote'][0]['open'][i],
                    "close": data['indicators']['quote'][0]['close'][i],
                    "volume": data['indicators']['quote'][0]['volume'][i],
                }
            )
        else :
            for i in range(0, len(data['timestamp'])):
                CompanyQuotes.append(
                    {
                        "date": newDate[i],
                        "high": data['indicators']['quote'][0]['high'][i],
                        "low": data['indicators']['quote'][0]['low'][i],
                        "open": data['indicators']['quote'][0]['open'][i],
                        "close": data['indicators']['quote'][0]['close'][i],
                        "volume": data['indicators']['quote'][0]['volume'][i],
                        "adjclose": data['indicators']['adjclose'][0]['adjclose'][i]
                    }
                )
        company = [data['meta']['symbol'] , CompanyQuotes ]
        return company






''' 

Method and Params: YahooFinance( Symbol , Range/Duration , interval )
$symbol is the stock ticker symbol, e.g. AAPL for Apple
$range/duration is the desired range of the query, allowed parameters are [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]
$interval is the desired interval of the quote, e.g. every 5 minutes, allowed parameters are [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3m

Ex : 
ytd = YahooFinance('AAPL', '1d', '1d')
quotes = ytd.CompanyQuotes()
print(quotes)

'''


















 
