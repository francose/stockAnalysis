import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



path = "Companies/"
headers = ['date',
           'open',
           'high',
           'low',
           'close',
           'adj_close',
           'vol']
class CompanyNames(object):

    def __init__(self, url, thickers=[], urlList=[], contentList=[]):
        self.url = url
        self.thickers = thickers
        self.urlList = urlList
        self.content = contentList

#gets the top 10 company thickers
    def getNames(self):
        result = requests.get(self.url).text
        rawHtml = BeautifulSoup(result, 'html.parser')
        rawThickers = rawHtml.select('tr > td > p > a')
        for i in range(0, len(rawThickers)):
            company = rawThickers[i].text
            self.thickers.append(company)
        return(self.thickers)

    def appendNames(self, urlList=[]):
        LIST = [self.urlList.append(self.url + i + "/history?p=" + i) for i in self.thickers]
        return(self.urlList)


    def getContent(self):
        for url in self.urlList:
            res = requests.get(url)
            data = res.content
            raw = BeautifulSoup(data, 'html.parser')
            tableBody = raw.findAll('table', attrs={'class': 'W(100%) M(0)'})
        self.getTableBody(tableBody[0])

    def getTableBody(self, table, data=[]):
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        dataFrame = pd.DataFrame(data, columns=headers)

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            # print(dataFrame)
            for i in self.thickers:
                with open(path + i + "/" + i + ".csv", "w+") as f:
                    f.writelines(str(dataFrame))
            
    def createDirectory(self):
        for dr in self.thickers:
            try:
                abspath = path + dr
                os.mkdir(abspath)
                open(abspath + "/" + dr + ".csv", "w+")
            except OSError:
                print("Creation of the directory %s failed" % dr)
            else:
                print("Successfully created the directory %s " % dr)


                
