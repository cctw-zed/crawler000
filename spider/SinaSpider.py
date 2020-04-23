from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
import requests
import urllib.request
import re

class SinaSpider(object):
    def __init__(self, keyword, pageNum=3, pageSize=10):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'cookie':'U_TRS1=00000017.744b2f8f.5dbffd90.ba54723f; SINAGLOBAL=111.175.187.165_1573808942.407626; UOR=www.google.com,k.sina.com.cn,; SUB=_2AkMqi0B7f8NxqwJRmPATxW_lZI12ygvEieKc17GgJRMyHRl-yD9jqhxYtRB6AQtulBGImBWaS9JGIjlE1TE1_wIW-VUR; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5bUYKwWx7ZBA4rKu_zNK8K; gr_user_id=f5c1aba3-bf65-469e-99df-5250f4d1a1c4; grwng_uid=7b1e1e98-d50e-4140-93bf-2250957fa098; lxlrttp=1578733570; _ga=GA1.3.964044520.1586607512; Apache=120.227.53.143_1587350196.645834; SGUID=1587350197642_36027557; ULV=1587350204230:7:3:2:120.227.53.143_1587350196.645834:1587350195658; beegosessionID=475e4350e68caa8956addc8f6ae0574c; WEB5_OTHER=46b25b3de5f6a383240081241697b716; _gid=GA1.3.296175008.1587366106'
    }

        self.keyword = keyword
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.connection = MyMongoDB()
        
    
    def getPage(self, pageIndex):
        url = 'https://search.sina.com.cn/'
        params = {
            'q': self.keyword,
            'c': 'news',
            'from': '',
            'col': '',
            'range': 'all',
            'source': '',
            'country': '',
            'size': 10,
            'stime': '',
            'etime':'',
            'time': '',
            'dpc': 0,
            'a': '',
            'ps': 0,
            'pf': 0,
            'page': pageIndex,
        }
        response = requests.get(url, headers=self.headers, params=params)

        if(response.status_code ==200):
            page = response.text
            self.parserPage(page)

        # print(page)
    def parserPage(self,page):
        # print(page)
        soup = BeautifulSoup(page, 'lxml')
        result = soup.find('div', attrs={'id': 'result'})
        content_list = result.find_all('div',attrs={'class': 'box-result clearfix'})

        for i in range(len(content_list)):
            try:
                content = content_list[i]
                res = {}
                res['title'] = content.find('a').text
                res['real_url'] = content.find('a').get('href')
                site_time = content.find('span',attrs ={'class': 'fgray_time'}).text.strip().split(' ')
                res['time'] = site_time[1] + ' ' + site_time[2]
                res['abstract'] =  content.find('p', attrs={'class':'content'}).text
                res['real_site'] = site_time[0]  #我加着玩的 用来
                res['site'] = '新浪网'
                res['keyword'] = self.keyword
                self.connection.insert(res)
            except:
                continue
    def run(self):
        for i in range(self.pageNum):
            sleep(2)
            self.getPage(i+1)
        
if __name__ == "__main__":
    spider = SinaSpider('疫情')
    spider.run()
    # page = spider.getContent('http://www.hnrd.gov.cn/Info.aspx?ModelId=1&Id=31707')
    # print(page)



