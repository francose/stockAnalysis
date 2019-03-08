import os, requests, time
from bs4 import BeautifulSoup


path = "Companies/"
class CompanyNames(object):
    def __init__(self, url, thickers=[], urlList=[]):
        self.url = url
        self.thickers = thickers
        self.urlList = urlList

#gets the top 10 company thickers
    def getNames(self):
        result = requests.get(self.url).text
        rawHtml = BeautifulSoup(result, 'html.parser')
        rawThickers = rawHtml.select('tr > td > p > a')
        for i in range(0, len(rawThickers)):
            company = rawThickers[i].text
            self.thickers.append(company)
        return(self.thickers)

    def createDirectory(self):
        if (os.path.exists(path)):
             print("The directory %s checked ...  " % path)
             time.sleep(.8)
             for dr in self.thickers:
                try:
                    abspath = path + dr
                    os.mkdir(abspath)
                    open(abspath + "/" + dr + ".csv", "w+")
                except OSError:
                    print("Creation of the directory %s failed" % dr)
                else:
                    print("Successfully created the directory %s " % dr)
                    time.sleep(.8)
        else:      
            print("The directory of %s does not exist ... now creating the directory" % path)
            time.sleep(.8)
            try:
                os.makedirs(path)
            except OSError:
                print('failed to create the directory ... please re-run the routine again ...')
            else:
                print("Successfully created the directory of %s" % path)
                time.sleep(.8)
                self.createDirectory()    

    def createURL(self):
        for i in self.thickers:
            self.urlList.append(self.url + i + "/history?p=" + i)
        return(self.urlList)






                




