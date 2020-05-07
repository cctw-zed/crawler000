from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import urllib.request
import re

class AnhuiSpider(object):
    def __init__(self, keyword, pageNum=4, pageSize=10):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        
    
    def getPage(self, pageIndex):
        url = 'http://www.ahrd.gov.cn/ahrdweb/search.jsp'
        params = {
            'strWebSiteId': 1448865560847002,
            'key': '',
            'strSearchColId': '',
            'sDate':'' ,
            'eDate':'' ,
            'strSearchContent': self.keyword.encode('GBK'),
            'PageSizeIndex': pageIndex,
        }
        try:
            response = requests.post(url, headers=self.headers, data=params)
            if(response.status_code ==200):
                page = response.text
                self.parserPage(page)
        except:
            pass
        # print(page)
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml')
        contents_list = soup.find('div', attrs={'class':'searchlist'}).find_all('li')
        # print(contents_list)
        for i in range(len(contents_list)):
            try:
                content = contents_list[i]
                # print(content)
                title = content.find('h4').text
                abstract = content.find('p').text
                time = content.find('div', attrs={'class':'list-botmsg'}).find('i').text
                hrefurl = 'http://www.ahrd.gov.cn/ahrdweb/' + content.find('a').get('href')
                res = {}
                res['title'] = title
                res['real_url'] = hrefurl
                # res['abstract'] = self.getContent(hrefurl)
                res['abstract'] = abstract
                res['time'] = time
                res['site'] = '安徽人大网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
            except:
                print('安徽人大解析出错')
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
    spider = AnhuiSpider('野生动物')
    spider.run()
    # page,time  = spider.getContent('http://www.ccpc.cq.cn/home/index/more/id/219342.html')
    # print(page)


 