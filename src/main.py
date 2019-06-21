
'''
Auhtor : Sadik Erisen

'''

import os
import requests
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
    "https://finance.yahoo.com/quote/",
    "http://www.barchart.com/stocks/sp500.php"
]


class AbstractFoundation(object):
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

    def write_ToCSV(self, path='output.csv'):
        if not path[-4:] == '.csv':
            path += '.csv'     
        self.dataframe.to_csv(path, index=True)



class ConsumeData(AbstractFoundation):

    def __init__(self, url, *args, **kwargs):
        super().__init__()
        self.url = url

    def reponseContent(self):
        result = self.url_RESPONSE(self.url).text
        raw = BeautifulSoup(result, 'html.parser')
        print(raw)
        return raw



#Methods
def Extractor(url):
    '''Exctractor method below gets raw html with given endpoint '''
    extract = ConsumeData(url)
    return extract.reponseContent()


if __name__ == "__main__":
    Extractor(ENDPOINTS[0])



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
 
