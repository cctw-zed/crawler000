from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import urllib.request
import re

class HunanSpider(object):
    def __init__(self, keyword, pageNum=1, pageSize=10):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.hnrd.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        
    
    def getPage(self, pageIndex):
        url = 'http://www.hnrd.gov.cn/search.aspx'
        params = {
           'chid':1,
           'fieldname':'title',
           'keyword':self.keyword,
           'p':pageIndex,
        }
        response = requests.get(url, headers=self.headers, params=params)
        if(response.status_code ==200):
            page = response.text
            self.parserPage(page)

        # print(page)
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml')
        # print(soup)
        trs = soup.find_all('tr',  attrs={'height': '22px'})
        for i in range(len(trs)):
            try:
                tr = trs[i]
                title = tr.find_all('a')[1].text
                hrefurl = 'http://www.hnrd.gov.cn'+ tr.find_all('a')[1].get('href')
                time = tr.find_all('td')[1].text
                res = {}
                res['title'] = title
                res['real_url'] = hrefurl
                # res['abstract'] = self.getContent(hrefurl)
                res['abstract'] = self.getContent(hrefurl)
                res['time'] = time
                res['site'] = '湖南人大网'
                res['keyword'] = self.keyword
                
                # self.connection.insert(res)
                print(res)
            except:
                continue

    def getContent(self, pageurl):
        try:
            rep = requests.get(pageurl, headers=self.headers)
            if rep.status_code == 200:
                try:
                    soup = BeautifulSoup(rep.text, 'lxml')
                    text = soup.find('div', attrs={'id': 'content'}).text.encode(rep.encoding).decode('utf-8')
                    text = re.sub('[[img].*[/img]]','',text)
                    return text
                except:
                    print('解析出错')
                    return ''

        except:
            print('出错了')
            return ''


    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i+1)

if __name__ == "__main__":
    spider = HunanSpider('疫情')
    spider.run()
    # page = spider.getContent('http://www.hnrd.gov.cn/Info.aspx?ModelId=1&Id=31707')
    # print(page)


 