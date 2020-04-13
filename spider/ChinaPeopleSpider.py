from time import sleep
from bs4 import BeautifulSoup
import requests
import urllib.request

class ChinaPeopleSpider(object):
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

    def getUrl(self,keyword,pageIndex):
        url = 'http://zs.kaipuyun.cn/s'
        params = {
            'searchWord': self.keyword,
            'column': '%E6%96%B0%E9%97%BB',
            'wordPlace': 0,
            'orderBy': 0,
            'startTime':'', 
            'endTime': '',
            'pageSize': self.pageSize,
            'pageNum': pageIndex,
            'timeStamp': 0,
            'siteCode': 'N000007903',
            'siteCodes':'', 
            'checkHandle': 1,
            'strFileType': '%E5%85%A8%E9%83%A8%E6%A0%BC%E5%BC%8F',
            'sonSiteCode': '',
            'areaSearchFlag': 0,
            'secondSearchWords': '',
            'countKey':  0,
            'left_right_index': 0,
        }
        response = requests.get(url,headers=self.headers, params=params)
        print(response)
        if(response.status_code == 200):
            self.parserPage(response.text)
            
    def parserPage(self,page):
        soup = BeautifulSoup(page,'lxml')
        divs = soup.find_all('div', attrs={'class':'wordGuide Residence-permit'})
        
        for div in divs:
            title = div.find('a').text
            hrefurl = div.find('a').get('href')
            content = div.find('p',attrs={'class': 'summaryFont'}).text
            time = div.find('p', attrs={'class': 'time'}).find('span', attrs={'class': 'sourceDateFont'}).text
            res = {}
            res['title'] = title
            res['real_url '] = hrefurl
            res['abstract'] = content
            res['time'] = time
            res['platform'] = '中国人大网'
            res['keyword'] = self.keyword
            print(res)

    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getUrl(self.keyword, i)

if __name__ == "__main__":
    spider = ChinaPeopleSpider('疫情')
    spider.run()


