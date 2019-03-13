import urllib.request, time, json
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
from globals import ENDPOINTS, URLS, HEADERS, PATH
from companyNames import CompanyDirectories

# NAMES = []
# compDics = CompanyDirectories(ENDPOINTS[1])
# names = compDics.getNames()
# def appendd():
#     x = 0
#     while x < len(names):
#         NAMES.insert(0,names[x])
#         x+=1
# appendd()


status = []
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
                status.insert(0,res[x].getcode())
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
        for i in range(0, len(rows)):
            cols = [ele.text.strip() for ele in rows[i].find_all('td')]
            self.data.insert(0,cols)
        self.frameObjects(self.data)

        
        
    def frameObjects(self, obj):
        with pd.option_context('display.max_rows', 200, 'display.max_columns', 200):
            dataFrame = pd.DataFrame(obj, columns=HEADERS) 
            dataFrame.dropna(inplace=True)
            
            status_df = pd.DataFrame(status, columns=["Status_Code"])
           
            name_df = pd.DataFrame(status, columns=["NAME"])

            result = pd.concat([status_df, name_df, dataFrame], axis=1)
            
            data = result.head(1).to_json(orient='records')
            print(data )
           
            

    # def appendTo(self, df): 
    
    #     for key in names:
    #         newPath = PATH + key + "/" + key + ".json"
    #         f = open(newPath, 'w')
    #         json.dump(df, f, indent=4)
            
                
            
            
            



    

