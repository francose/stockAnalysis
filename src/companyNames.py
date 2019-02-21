import os
import requests 
from bs4 import BeautifulSoup


class CompanyNames(object):
    
    def __init__(self, url, thickers=[], content=[]):
        self.url = url
        self.thickers = thickers
        self.content = content

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
        LIST = [self.content.append(self.url + i + "/history?p=" + i) for i in self.thickers]
        return(self.content)

    def createDirectory(self, company="Companies/"):
        for dr in self.thickers:
            try: 
                os.mkdir(company + dr)
                open(company + dr + "/"+ dr +".html", "w+")
            except OSError:
                print("Creation of the directory %s failed" % dr)
            else:
                print("Successfully created the directory %s " % dr)



