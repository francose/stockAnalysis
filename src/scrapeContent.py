from globals import *


class Scrape(object):
    def __init__(self, url, tag):
        self.url = url
        self.tag = tag   

    def createConnection(self):
        raw = urllib.request.urlopen(self.url)
        con = raw.getcode()
        print("Start : ",con ,self.tag,'\n', self.url)
        self.getContent(raw)

    def getContent(self, res):
        data = []
        bytesStrdata = res.read()
        strNew = bytesStrdata.decode('utf-8')
        raw = BeautifulSoup(strNew, 'html.parser')
        tableBody = raw.find_all('table', attrs={'class': 'W(100%) M(0)'})
        table_body = tableBody[0].find('tbody')
        rows = table_body.find_all('tr')
        for i in range(0, len(rows)):
            cols = [ele.text.strip() 
            for ele in rows[i].find_all('td')]
            data.insert(i, cols)
        return self.frameObjects(data)
        
    def frameObjects(self, obj):
        print(len(obj))
        with pd.option_context('display.max_rows', 200, 'display.max_columns', 200):
            dataFrame = pd.DataFrame(obj, columns=HEADERS).to_json(
                orient='records', lines=True)
            self.appendTo(dataFrame)
        return dataFrame
           
    def appendTo(self, df): 
        newPath = PATH + self.tag + "/" + self.tag + ".json"
        f = open(newPath, 'w')
        f.write(df)
        print('done...')
        f.close()
        
    
                
            
            
            



    


