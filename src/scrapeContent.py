import urllib.request, time
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
from globals import ENDPOINTS, URLS, HEADERS, PATH
from companyNames import CompanyDirectories

compDics = CompanyDirectories(ENDPOINTS[1])
names = compDics.getNames()


class Scrape:

    def getURL(self, x=0, pool=ThreadPool(32)):
        try:
            res = pool.map(urllib.request.urlopen, URLS)
        except urllib.error.HTTPError as e:
            print('HTTP ERR: {}'.format(e.code)) 
        except urllib.error.URLError as e:
            print('URLError: {}'.format(e.reason))
        else:
            while x < len(URLS):
                print('Status code : ' , res[x].getcode(), "\t", names[x]) 
                self.getContent(res[x])              
                pool.close()
                pool.join()   
                res[x].close()
                x += 1

            
    data = []
    def getContent(self, res):
        bytesStrdata = res.read()
        strNew = bytesStrdata.decode('utf-8')
        raw = BeautifulSoup(strNew, 'html.parser')
        tableBody = raw.find_all('table', attrs={'class': 'W(100%) M(0)'})
        table_body = tableBody[0].find('tbody')
        rows = table_body.find_all('tr')
        for i in range(0,len(rows)):
            cols = [ele.text.strip() for ele in rows[i].find_all('td')]
            self.data.append(cols)
        self.frameObjects(self.data)    
            
    def frameObjects(self, obj):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            dataFrame = pd.DataFrame(obj, columns=HEADERS)
            for key in names:
                filename = open(PATH + key + "/" + key + ".csv", "w")
                filename.write(str(dataFrame))
                filename.close()
            
            
            



    

