from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import re


class JiangxiPeopleSpider(object):
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
            'Host': 'search.jxnews.com.cn:7001',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

    def getPage(self, pageIndex):
        url = 'http://search.jxnews.com.cn:7001/m_fullsearch/searchurl/mfullsearchgj!hGDescResult.do'
        params = {
            'keywords': self.keyword,
            'keytitle': self.keyword,
            'sPubDate': '',
            'ePubDate': '',
            'channelId': '0',
            #'channelId': '0',
            'channel_id': '0',
            'size': '',
            'header': '',
            #'keywords': '',
            'footer': '',
            'orderFlg': '',
            'startPage': '',
            'endPage': '',
            'pageNoCurrent': pageIndex,
            'pageNoRecode': '',
            'allChannelId': '66000000000000000',
            'selectNum': '2'
            }
        response = requests.post(url, headers=self.headers, data=params)
        if response.status_code == 200:
            page = response.text
            self.parserPage(page)

    def parserPage(self, page):
        soup = BeautifulSoup(page, 'lxml')
        # item.get_text().split()
        # 0 代表 url
        # 1 代表 时间
        urlsandtimes = soup.findAll(attrs={'class': 'searchBotton'})
        # item.get_text(), 奇次项代表标题，偶次项代表序号（这里忽略不要）
        titles = soup.findAll(attrs={'class': 'searchTitle'})
        # abstracts[0].get_text().strip()
        abstracts = soup.findAll(attrs={'class': 'searchMain'})
        for i in range(len(urlsandtimes)):
            res = {}
            res["title"] = titles[2*i+1].get_text()
            res['real_url'] = urlsandtimes[i].get_text().split()[0]
            res['time'] = urlsandtimes[i].get_text().split()[1]
            res['abstract'] = abstracts[i].get_text().strip()
            res['keyword'] = self.keyword
            res['site'] = '江西人大网'
            #print(res)
            self.connection.insert(res)

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i + 1)


if __name__ == "__main__":
    op = JiangxiPeopleSpider("习近平")
    op.run()