import os
import requests
from bs4 import BeautifulSoup


path = "Companies/"
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
            tableBody = [ td.findAll('span') for td in raw.findAll(attrs={'data-test': 'historical-prices'})]
        self.getTableBody(tableBody)

    def getTableBody(self, tableBody, history=[]):
        table = [ history.append(table.text) for table in tableBody[0]]
        for row in range(0, len(table[7:697])):
            obj= {
                'date': history[row],
                'open': history[row],
                'high': history[row],
                'low': history[row],
                'close': history[row],
                'adj_close': history[row],
                'vol': history[row],
            }
            print(obj)

        # for i in self.thickers:
        #     with open(path + i + "/" + i + ".csv", "w+") as f:
        #         f.writelines(str(tbody))
            
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


 
