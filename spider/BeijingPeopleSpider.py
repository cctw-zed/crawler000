from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import re

class BeijingSpider(object):
    def __init__(self, keyword, pageNum=3, pageSize=10):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'sousuo.bjrd.gov.cn:8080',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        
  
    def getPage(self, pageIndex):
        url = 'http://sousuo.bjrd.gov.cn:8080/was5/web/search'
        params = {
            'page': pageIndex,
            'channelid': 237169,
            'searchword': self.keyword,
            'keyword': self.keyword,
            'orderby': '-docreltime',
            'token': '9.1350302879613.25',
            'perpage': self.pageSize,
            'outlinepage': 10,
            'andsen': '',
            'total': '',
            'orsen': '',
            'exclude': '',
            'timescope': '',
            'timescopecolumn':'', 
            'orderby': '-docreltime'
        }
        response = requests.get(url, headers=self.headers, params=params)
        if(response.status_code ==200):
            page = response.text
            self.parserPage(page)
        # print(page)
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml').find('div',  attrs={'class': 'search_con'})
        titles = soup.find_all('p', attrs={'class': 'search_con_title'})
        contents = soup.find_all('p', attrs={'class': 'search_con_txt'})
        dates = soup.find_all('p', attrs={'class': 'search_con_date'})
        for i in range(len(titles)):
            try:
                title = titles[i].text
                hrefurl = titles[i].find('a').get('href')
                if hrefurl == '':
                    continue
                content = contents[i].text
                date = re.findall(r'\t(.+?)\n',dates[i].text)[0].strip()
                res = {}
                res['title'] = title.strip()
                res['real_url'] = hrefurl
                res['abstract'] = content.strip()
                res['time'] = date
                res['site'] = '北京市人大网'
                res['keyword'] = self.keyword
                # self.connection.insert(res)
                print(res)
            except:
                continue
    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i)

if __name__ == "__main__":
    spider = BeijingSpider('大火')
    spider.run()



 