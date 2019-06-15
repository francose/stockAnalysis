'''
Auhtor : Sadik Erisen

'''

import globalAttribute as gb

class ScrapeData(object):

    def __init__(self, url):
        self.url = url

    def createConnection(self):
        try:
            raw = gb.urllib.request.urlopen(self.url)
            return raw
        except gb.urllib.error.URLError as e:
            print("connection err...%s", e)

    def reponseContent(self):    
        conn = self.createConnection()
        bytesStrdata = conn.read()
        strNew = bytesStrdata.decode('utf-8')
        raw = gb.BeautifulSoup(strNew, 'html.parser')
        return raw        

class NameOBJECTS(object):
    
    def __init__(self, raw):
        self.raw = raw

    def getNames(self):    
        tableBody = self.raw.findAll('a', attrs={"data-component": "link"})  
        data = [i.text for i in tableBody]
        return data
        

class UrlOBJECTS(object):

    def __init__(self, baseURL):
        self.baseURL = baseURL

    def createURLs(self, name=[]):
        urls = [self.baseURL + i +"/history?p="+i for i in name]
        return urls
        

class CompanyDirectories(object):
    def __init__(self, names):
        self.names = names

    def createDirectory(self):

        if (gb.os.path.exists(gb.PATH)):
            for dr in self.names:
                absPATH = gb.PATH + dr
                gb.os.mkdir(absPATH)
                open(absPATH + "/" + dr + ".json", "w+")
        else:
            print (
                "The directory of %s does not exist ... now creating the directory" % gb.PATH)
            try:
                gb.os.makedirs(gb.PATH)
                for dr in self.names:
                    absPATH = gb.PATH + dr
                    gb.os.mkdir(absPATH)
                    open(absPATH + "/" + dr + ".json", "w+")
            except OSError:
                print(
                    'failed to create the directory ... please re-run the routine again ...')
            else:
                print("Successfully created the directory of %s" %
                      gb.PATH)
                self.createDirectory()
                


scrp_name = ScrapeData(gb.ENDPOINTS[1])
__NAMES = NameOBJECTS(scrp_name.reponseContent())
__URL = UrlOBJECTS(gb.ENDPOINTS[0])
tags = __NAMES.getNames()

@gb.asyncio.coroutine
async def CreateDic():
    __DIR =  CompanyDirectories(tags)
    create__ =  __DIR.createDirectory()
    return create__
 

@gb.asyncio.coroutine
async def CreateURL():
    create_url = __URL.createURLs(tags)
    return create_url


class HistoricData:

    @classmethod
    async def call_List(cls, url):
        data = []
        response = await gb.aiohttp.ClientSession().get(url)
        # data = await response.text()
        bytesStrdata = await response.read()
        strNew = bytesStrdata.decode('utf-8')
        raw = gb.BeautifulSoup(strNew, 'html.parser')
        tables = raw.find_all('table', attrs={'class': 'W(100%) M(0)'})
        table_body = tables[0].find('tbody')
        rows = table_body.find_all('tr')
        for i in range(0, len(rows)):
            cols = [ele.text.strip()
            for ele in rows[i].find_all('td')]
            # data.insert(i, cols)
            print(cols)
        return data

    async def execute():
        urls = await CreateURL()
        futures = [HistoricData.call_List(url) for url in urls]
        await gb.asyncio.wait(futures)

#TODO In complete below: 
# class DFrame(object):

#     def __init__(self, object):
#         self.object = []


#     def frameObjects(self, obj):
#         with gb.pd.option_context('display.max_rows', 200, 'display.max_columns', 200):
#             dataFrame = gb.pd.DataFrame(obj, columns=gb.HEADERS).to_json()
#             self.object.append(dataFrame)
#         return dataFrame

#     def appendTo(self, df):
#         for tag in tags:
#             newPath = gb.PATH + tag + "/" + tag + ".json"
#             f = open(newPath, 'w')
#             f.write(df)
#             print('done...')
#             f.close()


async def main():
    if not (gb.os.path.exists("Companies/")):
        await gb.asyncio.gather(CreateDic(), HistoricData.execute(), CreateURL())
    else:
        gb.os.system("clear")
        print('files exist...')
        await gb.asyncio.gather(HistoricData.execute(), CreateURL())


if __name__ == "__main__":
    loop = gb.asyncio.get_event_loop()
    loop.run_until_complete(main())
 
