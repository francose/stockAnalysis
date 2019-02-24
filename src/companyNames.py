import os
import requests
from bs4 import BeautifulSoup



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
            tableHeader = raw.select('table > thead >tr >th')
        self.getTableHeaders(tableHeader)
        
    def getTableHeaders(self, tableHeader, path="Companies/"):
        headers = [i.text for i in tableHeader]
        for i in self.thickers:
            with open(path + i + "/" + i + ".csv", "w+") as f:
                f.writelines(str(headers))
        return(headers)
    
    def createDirectory(self, company="Companies/"):
        for dr in self.thickers:
            try:
                abspath = company + dr
                os.mkdir(abspath)
                open(abspath + "/" + dr + ".csv", "w+")
            except OSError:
                print("Creation of the directory %s failed" % dr)
            else:
                print("Successfully created the directory %s " % dr)


 
