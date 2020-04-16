from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import urllib.request
import re

class ChongqingSpider(object):
    def __init__(self, keyword, pageNum=1, pageSize=10):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        
    
    def getPage(self, pageIndex):
        url = 'http://www.ccpc.cq.cn/home/index/more/u/search/p/'+ str(pageIndex+1) + '.html'
        params = {
           'kwd':self.keyword,
        }
        response = requests.get(url, headers=self.headers, params=params)
        if(response.status_code ==200):
            page = response.text
            self.parserPage(page)

        # print(page)
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml')
        # print(soup)
        tagas = soup.find('ul', attrs ={'class': 'news_list'}).find_all('a')
        for i in range(len(tagas)):
            try:
                taga = tagas[i]
                title = taga.text
                hrefurl = 'http://www.ccpc.cq.cn/'+ taga.get('href')
                res = {}
                res['title'] = title
                res['real_url'] = hrefurl
                # res['abstract'] = self.getContent(hrefurl)
                res['abstract'], res['time'] = self.getContent(hrefurl)
                res['site'] = '重庆人大网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
            except:
                continue

    def getContent(self, pageurl):
        try:
            rep = requests.get(pageurl, headers=self.headers)
            if rep.status_code == 200:
                try:
                    soup = BeautifulSoup(rep.text, 'lxml')
                    # print(soup)
                    time = soup.find('div', attrs={'class': 'info'}).find('span').text.replace('时间：','').strip()
                    text = soup.find('div', attrs={'class':'text'}).text
                    # text = time
                    # text = soup.find('div', attrs={'class':' text'}).text
                    return text, time
                except:
                    print('解析出错')
                    return '', ''

        except:
            print('出错了')
            return '',''


    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i+1)

if __name__ == "__main__":
    spider = ChongqingSpider('疫情')
    spider.run()
    # page,time  = spider.getContent('http://www.ccpc.cq.cn/home/index/more/id/219342.html')
    # print(page)


 