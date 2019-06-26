
'''
Auhtor : Sadik Erisen
Version : 0.1
'''

import os, time, datetime, json ,six
from typing import Callable, List, Any

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


ENDPOINTS = [
    "https://query1.finance.yahoo.com/v8/finance/chart/"]


def sma(data, window):
    weight = np.repeat(1.0, window) / window
    avg = np.convolve(data, weight, mode='valid')
    # print("SMA:", avg)
    return avg


def ema(data, window):
    weight = np.exp(np.linspace(-1., 0., window))
    weight /= weight.sum()
    avg = np.convolve(data, weight, mode='full')[:len(data)]
    avg[:window] = avg[window]
    return avg


def discreteDiff(obj: List[float]) -> List[float]:
    series = pd.Series(obj)
    return series.diff(periods=14).dropna()

#reading data function, is just method that calucates the mean of the data and returns the value. Thought we need to manually pass the datafile.


def readData(Path):
    with pd.option_context('display.max_rows', 100, 'display.max_columns', 100):
        rawdata = pd.read_json(Path)
        df = pd.DataFrame(rawdata)
        # By replacing all the commas in number we can convert all the data point in to a float number type example: float(df['Close'][0].replace(",", ""))
        data = [float(df['Close'][i].replace(",", "")) for i in range(
            0, len(df['Close'].sort_values(ascending=True)))]
        #for both functions we pass the data as an array and set the window (period of 10)
        return data


def RSI(period=4):
    data = readData()
    e = ema(data, period)
    deltas = gb.np.diff(e)
    newArry = deltas[:period + 1]
    up = newArry[newArry >= 0].sum()/period
    down = -newArry[newArry < 0].sum() / period
    relativeStrenght = up/down
    rsi = gb.np.zeros_like(e)
    rsi[:period] = 100. - 100. / (1. + relativeStrenght)
    for i in range(period, len(e)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up*(period-1) + upval)/period
        down = (down*(period-1) + downval)/period
        rs = up//down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi


def macd(x=readData(), slow=25, fast=12):
    emaFast = ema(x, fast)
    emaSlow = ema(x, slow)
    print(emaFast, emaSlow, emaFast - emaSlow)
    return emaFast, emaSlow, emaFast - emaSlow




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





















 
