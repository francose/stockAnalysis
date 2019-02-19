#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'src'))
	print(os.getcwd())
except:
	pass

#%%
'''
pseudo code testing...
'''

import requests
from bs4 import BeautifulSoup
from multiprocessing import Process



ENDPOINTS = ["https://finance.yahoo.com/quote/","https://www.investopedia.com/articles/investing/053116/10-largest-holdings-sp-500-aaplamznfb.asp"]     


def createDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)



#gets the top 10 company thickers      
def getCompanyName():
    result = requests.get(ENDPOINTS[1])
    rawHtml = BeautifulSoup(result.text)
    rawThickers = rawHtml.select('tr > td > p > a')
    thickers = []
    for i in range(0,len(rawThickers)): 
        thickers.append(rawThickers[i].text)  
        createDirectory(rawThickers[i].text)
    return(thickers) 


#creates new urllist        
def appendNames(urlList=[]):
    companyNames = getCompanyName()
    LIST = [urlList.append( ENDPOINTS[0] + i +"/history?p="+ i ) for i in companyNames]
    return(urlList)

    
def getContent(domain):
    data = requests.get(domain)
    return(data.status_code)      




if __name__=='__main__':
    content_list = appendNames()
    x = 0
    for i in content_list:
        x += 1
        print('process', x)
        p = Process(target=getContent, args=(i, ))
        p.start()
        p.join()
     
  
   
    
    


#%%



