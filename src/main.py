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
from globals import ENDPOINTS

start = CompanyDirectories(ENDPOINTS[1])
CompanyList = CompanyDirectories(ENDPOINTS[0])
scrape = Scrape()

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
            scrape.getURL()
        except ImportError:
            start.getNames()
            Company()

              

def main():
    Company()
    

if __name__=='__main__':
    main()



#%%


