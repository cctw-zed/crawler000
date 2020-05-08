from time import sleep
import requests
from ConnectMongoDB import MyMongoDB
from bs4 import BeautifulSoup


class LiaoNingPeopleSpider(object):

    def __init__(self, keyword, pageNum=2, pageSize=15):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        # self.connection = MyMongoDB()
        self.baseUrl = 'http://www.lnrd.gov.cn/'


    def getResponse(self, keyword, pageIndex):
        baseUrl = self.baseUrl + 'search.html'
        params = {
            'keyword': self.keyword,
            'page': self.pageNum,
        }
        response = requests.get(baseUrl, params=params, headers=self.headers)
        if (response.status_code == 200):
            self.parseResponse(response)


    def parseResponse(self, response):
        # 此网站返回的是html
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        ul = soup.find('ul', attrs={'class': 'n-list', 'id': 'result'})
        # print(ul)
        lis = ul.find_all('li')
        for li in lis:
            try:
                a = li.find('a')
                # content =
                # time =
                res = {}
                res['title'] = a['title']
                res['real_url'] = self.baseUrl + a['href']
                res['abstract'] = li.find('p').get_text()
                res['time'] = li.find('div', attrs={'class': 'info'}).find('span').get_text()
                res['site'] = '辽宁人大网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
                #self.connection.insert(res)
                #print(res)
            except:
                continue


    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getResponse(self.keyword, i)

if __name__ == "__main__":
    spider = LiaoNingPeopleSpider('疫情')
    spider.run()