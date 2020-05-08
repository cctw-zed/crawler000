# from ConOfAllData import ConOfAllData
from time import sleep
from ES import ES
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
from urllib.parse import urljoin
import re

class JiangSuPeopleSpider(object):
    def __init__(self):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        # self.connection = ConOfAllData('jiangsu')
        # self.es = ES()
        self.es = ES('allspider')
        self.start_list = [
            'http://www.jsrd.gov.cn/sy/xw_syxw/',

            'http://www.jsrd.gov.cn/sy/xw_tpxw/',
            'http://www.jsrd.gov.cn/zsjs/jianshe_xx/',
            'http://www.jsrd.gov.cn/zsjs/zishen_lz/',
            'http://www.jsrd.gov.cn/zsjs/zishen_xxh/',

        ]
    # 抓取url得到response
    def crawl(self, url):
        time.sleep(0.3)
        # s = requests.session
        try:
            session = requests.session()
            response = session.get(url,headers=self.headers)
            if response.status_code == 200:
                session.close()
                return response
        except:
            session.close()
            return False

    # 解析栏目中的链接
    def parse(self, response,url):
        try:
            soup = BeautifulSoup(response.text)
            print(url)
            # print(soup)
            content = soup.find('div',attrs={'class':'newslist'})
            if content != None:
                tagas = content.find('ul').find_all('a')
            else:
                tagas = soup.find('div', attrs={'class':'piclist'}).find_all('a')
           
            for taga in tagas:
                try:
                    nowurl = urljoin(url,taga.get('href'))
                    title = taga.get_text()
                    if self.es.isExist(title):
                        continue
                    
                    # if self.connection.isexist(nowurl)==False:
                    rep = self.crawl(nowurl)
                    self.aimPageParse(rep,nowurl)
                except:
                    continue
        except Exception as e:
            print(e)
            print('解析栏目链接出错')
            pass


    def aimPageParse(self,rep, url):
        # print(contents_list)
        try:
            # print('开始解析目标页面了\n')
            soup = BeautifulSoup(rep.text,'lxml')
            # print(soup)
            res = {}
            res['title'] = soup.find('div',attrs={'id':'title'}).get_text()
            res['real_url'] = url
            # res['abstract'] = self.getContent(hrefurl)
            res['abstract'] = soup.find('div',attrs={'id':'content'}).get_text()
            res['time'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",soup.find('div', attrs={'id':'ptime'}).get_text()).group(0)[0:10]
            res['site'] = '江苏人大网'
            # self.connection.insert(res)
            self.es.InsertData(res)
            # print(res)
        except Exception as e:
            print(e)
            print('江苏人大网解析出错')
            pass
    
    def run(self):
        for item_url in self.start_list:
            try:
                for i in range(30):
                    if i==0:
                        url = urljoin(item_url, 'index.shtml')
                    else:
                        url = urljoin(item_url,'index_'+str(i)+'.shtml')
                    try:
                        rep = self.crawl(url)
                        if rep!=False and rep!=None:
                            self.parse(rep,url)
                    except:
                        continue
            except:
                continue
        # self.connection.end()
        

if __name__ == "__main__":
    Spider = JiangSuPeopleSpider()
    Spider.run()
    # rep = Spider.crawl('http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')
    # Spider.parse(rep,'http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')



 