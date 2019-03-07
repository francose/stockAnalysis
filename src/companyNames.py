import os
import requests, time
from bs4 import BeautifulSoup
import pandas as pd


path = "Companies/"
headers = ['Date',
           'Open',
           'High',
           'Low',
           'Close',
           'Adj Close',
           'Vol']
class CompanyNames(object):

    def __init__(self, url, thickers=[], urlList=[], body=[]):
        self.url = url
        self.thickers = thickers
        self.urlList = urlList
        self.body = body

#gets the top 10 company thickers
    def getNames(self):
        result = requests.get(self.url).text
        rawHtml = BeautifulSoup(result, 'html.parser')
        rawThickers = rawHtml.select('tr > td > p > a')
        for i in range(0, len(rawThickers)):
            company = rawThickers[i].text
            self.thickers.append(company)
        return(self.thickers)

    def appendNames(self):
        for i in self.thickers:
            self.urlList.append(self.url + i + "/history?p=" + i)  
        return(self.urlList)

    def getContent(self, x=0):
        for url in self.urlList:
            res = requests.get(url)
            data = res.content
            self.body.append(data)
            try:
                if(len(self.body) == 9 and res.status_code == 200):
                    for x in range (0, len(self.body)):
                        print(len(self.body), '/' , x)
                        # print(self.body[x], '\n\n')
                        raw = BeautifulSoup(self.body[x], 'html.parser')
                        tableBody = raw.findAll('table', attrs={'class': 'W(100%) M(0)'})
                        self.getTableBody(tableBody[0])
            except OSError: 
                    print('ERRR')
  


    def getTableBody(self, table, data=[]):
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
            dataFrame = pd.DataFrame(data, columns=headers)
        print(dataFrame.head(1), "\n done....")
        
    #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #         for i in self.thickers:
                # filename = open(path + i + "/" + i + ".csv", "w")
                # filename.write(str(dataFrame))
                # filename.close()
                # print(dataFrame.head(3))
                # print(path + i + "/" + i + ".csv", " is done ...")
                

            
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


                
