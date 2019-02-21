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
from companyNames import CompanyNames

ENDPOINTS = ["https://finance.yahoo.com/quote/",
             "https://www.investopedia.com/articles/investing/053116/10-largest-holdings-sp-500-aaplamznfb.asp"]


def main():
    Companies = CompanyNames(ENDPOINTS[1])
    Companies.getNames()
    Companies.createDirectory()


if __name__=='__main__':
    main()

   
    
     
  
   
    
    


#%%



