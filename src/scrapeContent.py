import urllib.request, time, json
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
from globals import *



class Scrape(object):
    def __init__(self, url, tag):
        self.url = url
        self.tag = tag   

    def createConnection(self):
        raw = urllib.request.urlopen(self.url)
        con = raw.getcode()
        print("Start : ",con ,self.tag,'\n', self.url)
        self.getContent(raw)

    data = []
    def getContent(self, res):
        bytesStrdata = res.read()
        strNew = bytesStrdata.decode('utf-8')
        raw = BeautifulSoup(strNew, 'html.parser')
        tableBody = raw.find_all('table', attrs={'class': 'W(100%) M(0)'})
        table_body = tableBody[0].find('tbody')
        rows = table_body.find_all('tr')
        for i in range(0, len(rows)):
            cols = [ele.text.strip() for ele in rows[i].find_all('td')]
            self.data.insert(0, cols)
        return self.frameObjects(self.data)
        
    def frameObjects(self, obj):
        with pd.option_context('display.max_rows', 200, 'display.max_columns', 200):
            dataFrame = pd.DataFrame(obj, columns=HEADERS, )
            dataFrame.dropna(inplace=True)
            dataFrame.rename(index={ i :  self.tag + ':%i'% i for i in range(0, len(NAMES))}, inplace=True)
            data = dataFrame.to_json(orient='index')
            self.appendTo(data)
            return data
           
    def appendTo(self, df): 
        newPath = PATH + self.tag + "/" + self.tag + ".json"
        f = open(newPath, 'w')
        f.write(df)
        print('done...')
        f.close()
        
    
                
            
            
            



    


