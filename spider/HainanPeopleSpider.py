from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import re

class HainanPeopleSpider(object):
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
            'Host': 'www.hainanpc.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

    def getPage(self, pageIndex):
        url = 'http://www.hainanpc.net/search/pcRender?pageId=f5261418ddc74f03b27e3590c531102b'
        params = {
            'originalSearchUrl': '/search/pcRender?pageId=f5261418ddc74f03b27e3590c531102b',
            'originalSearch': '',
            'app': 'f252ced9cb68460fb03cd0d2ec7d5748,29c0e27d2c8847beb1c53efd9e8e6504,acfa1407fb934fdba18cc4ca50ffe7cd,5f7be0ef31444fb38f2f30a9c784cd5f,fb08ee9869fa4ed09a243d34f6133ab8,ab265aca7e2d444a96a406b653753b5c,aab5497fa0b64c29bec9f854750b0b63,51c21eacd81e46cf87e592705abed4c3,ad9b4fc5189446e68c2e376250212169,9c54ed54860649cdbfc5857d2ee52784',
            'appName': '',
            'sr': 'score desc',
            'advtime': '',
            'advrange': '',
            'ext': '-siteId:1',
            'pNo': pageIndex,
            'searchArea': '',
            'advepq': '',
            'advoq': '',
            'adveq': '',
            'advSiteArea': '',
            'q': self.keyword
        }
        response = requests.post(url, headers=self.headers, data=params)
        if response.status_code == 200:
            page = response.text
            self.parserPage(page)

    def parserPage(self, page):
        soup = BeautifulSoup(page,'lxml')
        # 标题：item.find('h3').get_text().strip()
        titles = soup.findAll(attrs={'class': 'news-style1'})
        # 0代表网址：item.findAll('span')[0].get_text().strip()
        # 1代表时间：item.findAll('span')[1].get_text().strip()
        UrlAndTimes = soup.findAll('p', attrs={'class': 'dates'})
        # 摘要
        abstracts = soup.findAll('p', attrs={'class': 'txtCon hasImg'})
        for i in range(len(titles)):
            res = {}
            res["title"] = titles[i].find('h3').get_text().strip()
            res['real_url'] = UrlAndTimes[i].findAll('span')[0].get_text().strip()
            res['time'] = UrlAndTimes[i].findAll('span')[1].get_text().strip()
            res['abstract'] = abstracts[i].get_text().strip()
            res['keyword'] = self.keyword
            res['site'] = '海南人大网'
            # self.connection.insert(res)
            print(res)

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i + 1)


if __name__ == '__main__':
    op = HainanPeopleSpider("刘")
    op.run()