from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
from ConnectToElasticSearch import ConnectToElasticSearch
import requests
import re

class NingxiaPeopleSpider(object):
    def __init__(self, keyword, pageNum=3, pageSize=10):
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = ConnectToElasticSearch()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'search.nxnews.net:8080',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }


    def getPage(self, pageIndex):
        url = 'http://search.nxnews.net:8080/was5/web/search'
        params = {
            'page': pageIndex,
            'channelid': '294770',
            'searchword': self.keyword,
            'keyword': self.keyword,
            'was_custom_expr': '(' + self.keyword + ')',
            'perpage': '10',
            'outlinepage': '10',
            'searchscope': '',
            'timescope': '',
            'timescopecolumn':' ',
            'orderby': '',
            'andsen': '',
            'total': '',
            'orsen': '',
            'exclude': ''
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            page = response.text
            self.parserPage(page)

    def parserPage(self, page):
        soup = BeautifulSoup(page, 'lxml')
        pagelist = soup.findAll('div', attrs={'style': " text-align:left"})
        if len(pagelist) == 0:
            return
        i = 0
        while i < len(pagelist):
            res = {}
            res['title'] = pagelist[i].find('a').get_text()
            res['real_url'] = pagelist[i+1].find('a').get('href')
            abstractandtime = pagelist[i+1].get_text().split()
            res['abstract'], res['time'] = self.getabstractandtime(abstractandtime)
            res['site'] = '宁夏人大网'
            res['keyword'] = self.keyword
            i += 2
            # print(res)
            self.connection.insert(res)

    def getabstractandtime(self, alist):
        length = len(alist)
        if length < 5:
            return None, None
        else:
            time = alist[length-3] + " " + alist[length-2]
            abstract = ""
            for i in range(length-4):
                abstract += alist[i]
            return abstract, time

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i + 1)


if __name__ == "__main__":
    op = NingxiaPeopleSpider("疫情")
    op.run()