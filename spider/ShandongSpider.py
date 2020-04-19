from time import sleep
import requests
from ConnectMongoDB import MyMongoDB
from bs4 import BeautifulSoup


class HeilongjiangSpider(object):

    def __init__(self, keyword, pageNum=1, pageSize=10):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            # 'Cookie': '_gscu_804353707=87094750noeo8111; _gscbrs_804353707=1; UM_distinctid=171863806741db-0326e68a1fe3b-39687506-384000-171863806755bb; CNZZDATA1277756264=544091959-1587090157-http%253A%252F%252Fwww.hbrd.net%252F%7C1587101334; _gscs_804353707=t87102312kficlz91|pv:2',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        self.baseUrl = 'http://www.sdrd.gov.cn/'


    def getResponse(self, keyword, pageIndex):
        baseUrl = self.baseUrl + 'gentleCMS/cmssearch/search.do'
        params = {
            'siteId': '52c2bf3d-ae7b-4bbf-80e1-7a7d7fcbe130',
            'sort': '0',
            'start': '0',
            'size': '10',
            'channelId':'',
            'currentpage': pageIndex,
            'notword': '',
            'onetword': '',
            'content': keyword
        }
        response = requests.get(baseUrl, params=params, headers=self.headers)
        print(response.status_code)
        if (response.status_code == 200):
            self.parseResponse(response)
        else:
            print("山东请求失败")

    def parsePage(self, urls):
        for url in urls:
            try:
                response = requests.get(url, headers=self.headers)
                response.encoding='utf-8'
                soup = BeautifulSoup(response.text, 'lxml');
                # print(soup)
                title = soup.find('p', {'class': 'fs20 fcR fw'}).get_text()
                time = soup.find('p', {'class': 'fs12'}).get_text()
                abstract = soup.find('span', {'style': 'FONT-SIZE: 18px'}).get_text()

                res = {}
                res['title'] = title
                res['real_url'] = url
                res['abstract'] = abstract
                res['time'] = time
                res['site'] = '山东人大网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
                # print(res)
            except:
                print('山东人大爬取失败')

    def parseResponse(self, response):
        # 此网站返回的是html
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        list = soup.find_all('a', attrs={'style': 'text-decoration:underline;'}, recursive=True)
        urls = set()
        for a in list:
            urls.add(a['href'])
        print(urls)
        self.parsePage(urls)


    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getResponse(self.keyword, i)

if __name__ == "__main__":
    spider = HeilongjiangSpider('疫情')
    spider.run()
