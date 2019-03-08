import requests, time
from bs4 import BeautifulSoup
import pandas as pd

headers = ['Date',
           'Open',
           'High',
           'Low',
           'Close',
           'Adj Close',
           'Vol']

class Scrape(object):
    def __init__(self, url):
        self.url = url

    def getURL(self):
        res = requests.get(self.url)
        if not (res.status_code == 200):
            print(" %s is failed proceed to next one..." % self.url)
            time.sleep(.5)
            next(self.getContent(res))
        else:
            self.getContent(res)

    def getContent(self, res, data=[], x=0):
        data = res.content
        raw = BeautifulSoup(data, 'html.parser')
        tableBody = raw.find_all(
            'table', attrs={'class': 'W(100%) M(0)'})
        table_body = tableBody[0].find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            raw=([ele for ele in cols if ele])
            df = pd.DataFrame(raw)
            print(df)
            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     for i in self.thickers:
            #         filename = open(path + i + "/" + i + ".csv", "w")
            #         filename.write(str(dataFrame))
            #         filename.close()





