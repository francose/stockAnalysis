import globalAttribute as gb


class CompanyDirectories(object):
    def __init__(self, url, thickers=[]):
        self.url = url
        self.thickers = thickers
        

#gets the top 10 company thickers
    def getNames(self):
        result = gb.requests.get(self.url).text
        rawHtml = gb.BeautifulSoup(result, 'html.parser')
        rawThickers = rawHtml.select('tr > td > p > a')
        for i in range(0, len(rawThickers)):
            company = rawThickers[i].text
            self.thickers.append(company)   
        return(self.thickers)

    def createNAMES(self, name="NAMES="):
         f = open("globals.py", "a+")
         f.write(name+str(self.thickers)+'\n')
         f.close()


    def createURLS(self, url="URLS="):
        urls = [gb.ENDPOINTS[0]+tag+"/history?p=" + tag for tag in self.thickers]
        f = open("globals.py", "a+")
        f.write(url+str(urls))
        f.close()
       

        
       
    def createDirectory(self):
        if (gb.os.path.exists(gb.PATH)):
             print("The directory %s checked ...  " % gb.PATH)
          
             for dr in self.thickers:
                try:
                    absPATH = gb.PATH + dr
                    gb.os.mkdir(absPATH)
                    open(absPATH + "/" + dr + ".json", "w+")
                except OSError:
                    print("Creation of the directory %s failed" % dr)
                else:
                    print("Successfully created the directory %s " % dr) 
                    self.createNAMES()
                    self.createURLS()
        else:      
            print("The directory of %s does not exist ... now creating the directory" % gb.PATH)   
            try:
                gb.os.makedirs(gb.PATH)
            except OSError:
                print('failed to create the directory ... please re-run the routine again ...')
            else:
                print("Successfully created the directory of %s" % gb.PATH)
                self.createDirectory()

             
                
       
   
    






                




