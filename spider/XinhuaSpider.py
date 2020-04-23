from time import sleep
import requests
from ConnectMongoDB import MyMongoDB
import json

class XinhuaSpider(object):

    def __init__(self, keyword, pageNum=3, pageSize=10):
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        self.baseUrl = 'http://so.news.cn/getNews'

    def getResponse(self, keyword, pageIndex):
        baseUrl = self.baseUrl
        params = {
            'keyword': self.keyword,
            'curPage': pageIndex,
            'sortField': 0,
            'searchField': 1,
            'lang': 'cn',
        }
        response = requests.get(baseUrl, params=params, headers=self.headers)
        if (response.status_code == 200):
            self.parseResponse(response)

    def parseResponse(self, response):
        # 此网站返回的是json字符串
        # print(soup)
        page = json.loads(response.text)
        content = page['content']
        results = content['results']

        for result in results:
            try:
                res = {}
                res['title'] = result['title']
                res['real_url'] = result['url']
                res['abstract'] = result['des']
                res['time'] = result['pubtime']
                res['site'] = result['sitename']
                res['keyword'] = self.keyword
                self.connection.insert(res)
                # print(res)
            except:
                continue

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getResponse(self.keyword, i)

if __name__ == "__main__":
    spider = XinhuaSpider('森林')
    spider.run()

