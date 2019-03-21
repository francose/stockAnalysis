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
import globalAttribute as gb


start = CompanyDirectories(gb.ENDPOINTS[1])
CompanyList = CompanyDirectories(gb.ENDPOINTS[0])


def validateVars():
    try:
        names = gb.NAMES
        urls = gb.URLS
        print('name list found %s' % names)
        print('url list found %s' % urls)
    except AttributeError:
        print ('var not found')
        start.createNAMES()
        start.createURLS()



def scrp():
    for i in range(0, len(gb.NAMES)):
        scrape = Scrape(gb.URLS[i], gb.NAMES[i])
        scrape.createConnection()
        print('process done..')
        # await asyncio.time(0.01)

 
def Company():
    if not (gb.os.path.exists("Companies/")):
        start.getNames()
        validateVars()
        start.createDirectory()
        Company()
    else:
        gb.os.system("clear")
        print('files exist...')
        scrp()
    

def main():
    Company()
    # readData()
   

    
    

if __name__=='__main__':
    main()



#%%

