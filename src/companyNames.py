import os, requests, time
from bs4 import BeautifulSoup
from globals import ENDPOINTS, URLS, HEADERS, PATH


class CompanyDirectories(object):
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
        if (os.path.exists(PATH)):
             print("The directory %s checked ...  " % PATH)
             time.sleep(.8)
             for dr in self.thickers:
                try:
                    absPATH = PATH + dr
                    os.mkdir(absPATH)
                    open(absPATH + "/" + dr + ".csv", "w+")
                except OSError:
                    print("Creation of the directory %s failed" % dr)
                else:
                    print("Successfully created the directory %s " % dr)
                    time.sleep(.8)
        else:      
            print("The directory of %s does not exist ... now creating the directory" % PATH)
            time.sleep(.8)
            try:
                os.makedirs(PATH)
            except OSError:
                print('failed to create the directory ... please re-run the routine again ...')
            else:
                print("Successfully created the directory of %s" % PATH)
                time.sleep(.8)
                self.createDirectory()    

    # def createURL(self):
    #     f = open("Companies/URL.txt", 'w+')
    #     for i in self.thickers:
    #         f.write('"' + self.url + i + "/history?p=" + i + '",\n')
    






                




