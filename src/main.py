#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting

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
from calculations import *
from globals import *


from multiprocessing import Pool

start = CompanyDirectories(ENDPOINTS[1])
CompanyList = CompanyDirectories(ENDPOINTS[0])
# graph = drawGraph()

def scrp():
    for i in range(0, len(NAMES)):
        scrape = Scrape(URLS[i], NAMES[i])
        scrape.createConnection()
 
def Company(name=getattr(globals, 'NAMES', None),
            url=getattr(globals, 'URLS', None)):

    if not (os.path.exists("Companies/")):
        start.getNames()
        start.createDirectory()
        Company()
        if( name is None and url is None):
            start.createNAMES()
            start.createURLS()
        else:
            Company()
    else:
        os.system("clear")
        print('files exist...')
        scrp()
    

def main():
    # Company()
    readData()

    
    

if __name__=='__main__':
    main()



#%%

