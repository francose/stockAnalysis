import requests 
from bs4 import BeautifulSoup


class CompanyNames(object):
    
    def __init__(self, url, thickers=[]):
        self.url = url
        self.thickers = thickers

#gets the top 10 company thickers
    def getNames(self):
        result = requests.get(self.url).text
        rawHtml = BeautifulSoup(result, 'html.parser')
        rawThickers = rawHtml.select('tr > td > p > a')
        for i in range(0, len(rawThickers)):
            company = rawThickers[i].text
            self.thickers.append(company)
        print(self.thickers)
        return(self.thickers)


