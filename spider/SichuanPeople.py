from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import re

class SichuanPeopleSpider(object):
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
            'Host': 'www.scspc.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

    def getPage(self, pageIndex):
        url = 'http://www.scspc.gov.cn/scrdsearch/search_do.jsp'
        params = {
            'docTitle': self.keyword,
            'page': pageIndex
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            page = response.text
            self.parserPage(page)

    def parserPage(self, page):
        soup = BeautifulSoup(page,'lxml')
        tables = soup.findAll('a')
        times = soup.find_all('span')
        for i in range(len(times)):
            res = {}
            title = tables[i*2].get_text().strip()
            res["title"] = title
            real_url = tables[i*2 + 1].get_text().strip()
            res["real_url"] = real_url
            time = times[i].get_text().strip()
            res["time"] = time
            res["site"] = "四川人大网"
            content = self.get_content(real_url)
            res["abstract"] = content
            res["keyword"] = self.keyword
            self.connection.insert(res)
            #print(res)

    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            page = response.text
            soup = BeautifulSoup(page, 'lxml')
            paragraphs = soup.findAll('p')
            content = ""
            for i in range(1, len(paragraphs)):
                temp = paragraphs[i].get_text().strip()
                if temp != "":
                    content += temp + '\n'
            return content

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i + 1)

if __name__ == "__main__":
    op = SichuanPeopleSpider("疫情")
    op.run()