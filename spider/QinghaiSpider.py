from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import urllib.request
import re

class Qinghai(object):
    def __init__(self, keyword, pageNum=3, pageSize=10):
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
        url = 'http://www.qhrd.gov.cn/search/Default.aspx?q='+self.keyword+'&ie=utf-8&portalid=1&image.x=0&image.y=0'
        params = {
           '__EVENTTARGET': 'GridView1',
           '__EVENTARGUMENT': 'Page$'+str(pageIndex),
           'TextBox1': self.keyword,

        }
        response = requests.post(url, headers=self.headers)
        if(response.status_code ==200):
            page = response.text
            self.parserPage(page)

        # print(page)
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml')
        contents = soup.find('ul',  attrs={'class': 'search-list'}).find_all('li')
        # print(contents)
        # for i in range(len(contents)):
        #     try:
        #         content = contents[i]
        #         title = content.find('a').text.strip()

        #         hrefurl = content.find('a').get('href')
   
        #         abstract = content.find('p').text.strip()
            
        #         time = content.find('span').text
        

        #         res = {}
        #         res['title'] = title
        #         res['real_url'] = hrefurl
        #         # res['abstract'] = self.getContent(hrefurl)
        #         res['abstract'] = abstract
        #         res['time'] = time
        #         res['site'] = '山西人大网'
        #         res['keyword'] = self.keyword
        #         # self.connection.insert(res)
        #         print(res)
        #     except:
        #         continue

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i+1)
if __name__ == "__main__":
    spider = Qinghai('疫情')
    spider.run()
    # page = spider.getContent('http://www.hnrd.gov.cn/Info.aspx?ModelId=1&Id=31707')
    # print(page)


 