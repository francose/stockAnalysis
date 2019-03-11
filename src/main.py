#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
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


ENDPOINTS = ["https://finance.yahoo.com/quote/",
             "https://www.investopedia.com/articles/investing/053116/10-largest-holdings-sp-500-aaplamznfb.asp"]


start = CompanyDirectories(ENDPOINTS[1])
CompanyList = CompanyDirectories(ENDPOINTS[0])

def Company():
    if not (os.path.exists("Companies/")):
        start.getNames()
        start.createDirectory()
        Company()
    else:
        os.system("clear")
        print('files exist')
        names = start.getNames()
        scrape = Scrape()
        scrape.getURL()
        for i in names:
            scrape.getName(i)

        

def main():
    Company()

if __name__=='__main__':
    main()



#%%


