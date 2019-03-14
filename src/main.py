#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os, time
try:
	os.chdir(os.path.join(os.getcwd(), 'src'))
	print(os.getcwd())
except:
	pass

#%%
'''
author : Sadik Erisen
'''

from companyNames import CompanyDirectories
from scrapeContent import Scrape
from globals import *

start = CompanyDirectories(ENDPOINTS[1])
CompanyList = CompanyDirectories(ENDPOINTS[0])

def scrp():
    for i in range(0, len(NAMES)):
        scrape = Scrape(URLS[i], NAMES[i])
        scrape.createConnection()

def Company():
    if not (os.path.exists("Companies/")):
        start.getNames()
        start.createDirectory()
        Company()
    else:
        os.system("clear")
        print('files exist...')
        try:
            print('globals exist...')
            scrp()
            time.sleep(1)
        except ImportError:
            start.getNames()
            Company()

              

def main():
    Company()
    

if __name__=='__main__':
    main()



#%%

    # def getURL(self, x=0, pool=ThreadPool(32)):
    #     try:
    #         res = pool.map(urllib.request.urlopen, URLS)
    #     except urllib.error.HTTPError as e:
    #         print('HTTP ERR: {}'.format(e.code))
    #     except urllib.error.URLError as e:
    #         print('URLError: {}'.format(e.reason))
    #     else:
    #         while x < len(URLS):
    #             status.insert(0, res[x].getcode())
    #             self.getContent(res[x])
    #             pool.close()
    #             pool.join()
    #             res[x].close()
    #             x += 1
