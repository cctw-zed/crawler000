from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
from ConnectToElasticSearch import ConnectToElasticSearch
import requests
import urllib.request
import re

class ShanghaiSpider(object):
    def __init__(self, keyword, pageNum=3, pageSize=10):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = ConnectToElasticSearch()

    
    def getPage(self, pageIndex):
        url = 'http://searchgov1.eastday.com/searchspscs/search.ashx'
        params = {
            'q': self.keyword.encode('GBK'),
            'page': pageIndex,
            'stype': 2,
            'sort': 2,
            'mp': 41,
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if(response.status_code ==200):
                page = response.text
                self.parserPage(page)
        except:
            pass
        # print(page)
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml')
        items = soup.find_all('div', attrs={'class':'resultItem'})
        for i in range(len(items)):
            try:
                item = items[i]
                title_and_url= item.find('a')
                title = title_and_url.get_text()
                hrefurl = title_and_url.get('href')

                time = item.find('font').get_text().split(' ')[1]
                content = item.find('div').get_text()
    
                res = {}
                res['title'] = title
                res['real_url'] = hrefurl
                # res['abstract'] = self.getContent(hrefurl)
                res['abstract'] = content
                res['time'] = time
                res['site'] = '上海人大网'
                res['keyword'] = self.keyword
                # self.connection.insert(res)
                print(res)
            except:
                print('上海人大解析出错')
                continue

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i+1)

if __name__ == "__main__":
    spider = ShanghaiSpider('疫情')
    spider.run()
    # page,time  = spider.getContent('http://www.ccpc.cq.cn/home/index/more/id/219342.html')
    # print(page)


 