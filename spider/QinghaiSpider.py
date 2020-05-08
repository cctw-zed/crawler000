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
        soup = BeautifulSoup(page, 'lxml')
        # print(soup)
        list1 = soup.find_all('a', attrs={'class': 'lan14'},recursive=True)
        # print(list1)
        list2 = soup.find_all('td', attrs= {'class': 'hei12'})
        # print(list2)
        for index in range(len(list1)):
            try:
                res = {}
                res['title'] = list1[index].text.strip()
                res['real_url'] = list1[index].get('href')
                res['abstract'] = list2[2*index].text.strip()
                time= list2[2*index+1].text.strip()
                time = time.split('\xa0\xa0\xa0')[1]
                res['time'] = time
                res['site'] = '青海人大网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
                #print(res)
            except:
                continue
    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i+1)
        
if __name__ == "__main__":
    spider = Qinghai('疫情')
    spider.run()
    # page = spider.getContent('http://www.hnrd.gov.cn/Info.aspx?ModelId=1&Id=31707')
    # print(page)



