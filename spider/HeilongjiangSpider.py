from time import sleep
import requests
from ConnectMongoDB import MyMongoDB
from bs4 import BeautifulSoup


class HeilongjiangSpider(object):

    def __init__(self, keyword, pageNum=2, pageSize=20):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': '_gscu_804353707=87094750noeo8111; UM_distinctid=171863806741db-0326e68a1fe3b-39687506-384000-171863806755bb; _gscbrs_804353707=1; CNZZDATA1277756264=544091959-1587090157-http%253A%252F%252Fwww.hbrd.net%252F%7C1587520867; _gscs_804353707=t87523246rob4sy20|pv:3',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        self.baseUrl = 'http://www.hljrd.gov.cn/'


    def getResponse(self, keyword, pageIndex):
        baseUrl = self.baseUrl + 'web/site/search.html'
        params = {
            'keywords': keyword,
            'page': pageIndex,
        }
        print('begin')
        response = requests.get(baseUrl, params=params, headers=self.headers)
        print(response)
        # print(response.status_code)
        if (response.status_code == 200):
            self.parseResponse(response)
        else:
            print("黑龙江请求失败")


    def parseResponse(self, response):
        # 此网站返回的是html
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        div = soup.find('div', attrs={'class': 'lingdao_search_list'}, recursive=True)
        ul = div.find('ul')
        lis = ul.find_all('li')
        divs = ul.find_all('div')

        for index in range(len(lis)):
            try:
                res = {}
                res['title'] = lis[index].find('a')['title']
                res['real_url'] = self.baseUrl + lis[index].find('a')['href']
                res['abstract'] = divs[index].find('a').get_text()
                res['time'] = lis[index].find('span').get_text()
                res['site'] = '黑龙江人大网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
                print(res)
            except:
                continue


    def run(self):
        for i in range(self.pageNum):
            sleep(0.5)
            try:
                self.getResponse(self.keyword, i)
            except:
                continue

if __name__ == "__main__":
    spider = HeilongjiangSpider('疫情')
    spider.run()
