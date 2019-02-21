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


start = CompanyNames(ENDPOINTS[1])
CompanyList = CompanyNames(ENDPOINTS[0])

def main():
    start.getNames()
    start.createDirectory()
    CompanyList.appendNames()


if __name__=='__main__':
    main()


#%%



