from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import re

class FujianPeopleSpider(object):
    def __init__(self, keyword, pageNum=3, pageSize=10):
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'www.fjrd.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

    def getPage(self, pageIndex):
        url = 'http://www.fjrd.gov.cn/search'
        params = {
            'author': '',
            'source': '',
            'infoType': '1',
            'beginTime': '',
            'endTime': '',
            'ctTitle': self.keyword,
            'pageNumber': pageIndex
        }
        response = requests.post(url, headers=self.headers, data=params)
        if response.status_code == 200:
            page = response.text
            self.parserPage(page)

    def parserPage(self, page):
        soup = BeautifulSoup(page, 'lxml')
        pagelist = soup.find('div', attrs={'class': 'list_segj'}).findAll('li')
        print(len(pagelist))
        for item in pagelist:
            res = {}
            res["title"] = item.find('a').get('title')
            real_url = "http://www.fjrd.gov.cn" + item.find('a').get('href')
            res['real_url'] = real_url
            res['time'] = item.find('span').get_text()
            res['abstract'] = self.get_content(real_url)
            res['keyword'] = self.keyword
            res['site'] = ' 福建人大网'
            # self.connection.insert(res)
            print(res)

    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            page = response.text
            soup = BeautifulSoup(page, 'lxml')
            paragraphs = soup.find('div', attrs={'class': 'detail_con'}).findAll('p')
            res = ""
            for item in paragraphs:
                res += item.get_text().strip() + "\n"
            return res

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i + 1)


if __name__ == '__main__':
    op = FujianPeopleSpider("习近平")
    op.run()
