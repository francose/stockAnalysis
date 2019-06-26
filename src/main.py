
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
    "http://www.barchart.com/stocks/sp500.php"

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


class BarChart_SNP500(AbstractComsumer):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def percentage_string_to_number(self, df, columns, type_='float'):
        if not isinstance(columns, list):
            columns = [columns]
        for column in columns:
            df[column].replace('\+|%', '', regex=True, inplace=True)
            df[column].replace('unch', '0', inplace=True)
            df[column] = df[column].astype(type_) / 100
            return df[column]

    def getContent(self, url):
        html = self.fetch(url).content
        raw = BeautifulSoup(html, 'html.parser')
        return raw

    def extract_data(self, raw, columns):
        """extract table data from soup, returns dataframe"""
        data = []
        tbody = raw.find('table', attrs={'id': 'dt1'}).tbody
        rows = tbody.findAll('tr')
        for row in rows:
            cells = row.findAll('td')
            record = [cells[i].text.strip() for i in range(len(columns))]
            data.append(record)

        df = pd.DataFrame(data, columns=columns)
        df.set_index('Symbol', inplace=True)
        df.replace('N/A', 0)
        return df

    def collect_snp500_by_type(self, type_='main'):
        """get snp500 data and store in dataframe.
        There are three types of data:
        main, technical, and performance
        """
        columns = ['Symbol', 'Name', 'Last']
        qs = {'view': 'main', '_dtp1': 0}
        pct_columns = []  # percentage string columns need to be cleaned up
        if type_ == 'main':
            columns += ['Change', 'Percent', 'High', 'Low', 'Volume', 'Time']
            pct_columns = ['Percent']
        elif type_ == 'technical':
            columns += ['Opinion', '20D-Strength',
                        '20D-Volty', '20D-AVol', '52W-Low', '52W-High']
            qs.update({'view': 'technical'})
            pct_columns = ['20D-Strength', '20D-Volty']
        elif type_ == 'performance':
            columns += ['W-Alpha', 'YTD-Pct', '1M-Pct', '3M-Pct', '1Y-Pct']
            qs.update({'view': 'performance'})
            pct_columns = ['YTD-Pct', '1M-Pct', '3M-Pct', '1Y-Pct']

        content = self.getContent(ENDPOINTS[1])
        dataFrame = self.extract_data(content, columns)
        self.percentage_string_to_number(dataFrame, pct_columns)

        # Add date to dataframe
        dataFrame['Date'] = datetime.date.today()

        if self.dataframe is None:
            self.df = dataFrame
        else:
            columns_to_use = dataFrame.columns.difference(self.df.columns)
            self.df = self.df.join(dataFrame[columns_to_use])
        return dataFrame

    def snp500_full_data(self):
        """get combines three types of data into single dataframe"""
        for view in ['main', 'technical', 'performance']:
            self.collect_snp500_by_type(view)

    def snp500_symbol_list(self):
        """return the list S&P 500 company symbols"""
        if self.df is None:
            self.collect_snp500_by_type('main')
        return self.df.index.values.tolist()



        

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


















 
