from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import urllib.request
import re

class HubeiSpider(object):
    def __init__(self, keyword, pageNum=3, pageSize=10):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.hppc.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        
    def getContent(self, pageurl):
        try:
            rep = requests.get(pageurl, headers=self.headers)
            if rep.status_code == 200:
                try:
                    soup = BeautifulSoup(rep.text, 'lxml')
                    print(soup)
                    print(rep.encoding)
                    text = soup.find('div', attrs={'id': 'endtext'}).text.encode(rep.encoding).decode('utf-8')
                    return text
                except:
                    print('解析出错')
                    return ''

        except:
            print('出错了')
            return ''

    def getPage(self, pageIndex):
        url = 'http://www.hppc.gov.cn/list.php'
        params = {
            'eyword': self.keyword,
            'catid': 54,
            'x': 20,
            'y': 10,
            'page':pageIndex,
        }
        response = requests.get(url, headers=self.headers, params=params)
        if(response.status_code ==200):
            page = response.text
            self.parserPage(page)
        # print(page)
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml')
        # print(soup)
        titles = soup.find_all('div',  attrs={'class': 'list1'})
        for i in range(len(titles)):
            try:
                title = titles[i].find('a').text

                hrefurl = 'http://www.hppc.gov.cn'+ titles[i].find('a').get('href')
                time = titles[i].find('span').text

                res = {}
                res['title'] = title
                res['real_url'] = hrefurl
                res['abstract'] = self.getContent(hrefurl)
                res['time'] = time
                res['site'] = '湖北人大网'
                res['keyword'] = self.keyword
                # self.connection.insert(res)
                print(res)
            except:
                continue
    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i)

if __name__ == "__main__":
    spider = HubeiSpider('大火')
    # spider.run()
    page = spider.getContent('http://www.hppc.gov.cn/2020/0413/33001.html')
    print(page)


 