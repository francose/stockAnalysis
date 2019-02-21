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

from companyNames import CompanyNames

ENDPOINTS = ["https://finance.yahoo.com/quote/",
             "https://www.investopedia.com/articles/investing/053116/10-largest-holdings-sp-500-aaplamznfb.asp"]


def main():
    name = CompanyNames(ENDPOINTS[1])
    name.getNames()


if __name__=='__main__':
    main()

   
    
     
  
   
    
    


#%%



