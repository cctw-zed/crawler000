from time import sleep
import requests
from ConnectMongoDB import MyMongoDB
from bs4 import BeautifulSoup


class GuangxiPeopleSpider(object):

    def __init__(self, keyword, pageNum=1, pageSize=30):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'UM_distinctid=1717dc83b8bba-083667c3d56fbc-39687506-384000-1717dc83b8c655; CNZZDATA1254190265=781279961-1586950400-https%253A%252F%252Fcn.bing.com%252F%7C1587552978',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        self.baseUrl = 'https://www.gxrd.gov.cn/'


    def getResponse(self, keyword, pageIndex):
        baseUrl = self.baseUrl + 'search.php'
        params = {
            'keyword': keyword.encode('GBK'),
            'pageno': pageIndex,
        }
        response = requests.get(baseUrl, params=params, headers=self.headers)
        print(response.status_code)
        if (response.status_code == 200):
            self.parseResponse(response)


    def parseResponse(self, response):
        # 此网站返回的是html
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        div = soup.find('div', attrs={'class': 'm_list dborder'})
        # print(ul)
        lis = div.find('ul').find_all('li')
        for li in lis:
            try:
                span = li.find('span')
                a = li.find('a')
                res = {}
                res['title'] = a.get_text()
                res['real_url'] = self.baseUrl + a['href']
                res['abstract'] = res['title']
                res['time'] = span.get_text()
                res['site'] = '广西人大网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
                # print(res)
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
    spider = GuangxiPeopleSpider('疫情')
    spider.run()
