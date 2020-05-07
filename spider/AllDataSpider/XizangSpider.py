# from ConOfAllData import ConOfAllData
from ES import ES
from time import sleep
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
from urllib.parse import urljoin
import re

class XizangSpider(object):
    def __init__(self):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        # self.connection = ConOfAllData('xizang')
        # self.es = ES()
        self.es = ES('spider')
        self.start_list = [
            'http://www.xizangrd.gov.cn/List/19-{}.htm',
            'http://www.xizangrd.gov.cn/List/4-{}.htm',
            'http://www.xizangrd.gov.cn/List/3-{}.htm',
            'http://www.xizangrd.gov.cn/List/2-{}.htm',
            'http://www.xizangrd.gov.cn/List/33-{}.htm',
            'http://www.xizangrd.gov.cn/List/39-{}.htm',
            'http://www.xizangrd.gov.cn/List/35-{}.htm',
            'http://www.xizangrd.gov.cn/List/23-{}.htm',
            'http://www.xizangrd.gov.cn/List/24-{}.htm',
            'http://www.xizangrd.gov.cn/List/38-{}.htm',
            'http://www.xizangrd.gov.cn/List/22-{}.htm',


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
            # print(soup)
            content = soup.find('div',attrs={'class':'list_wrap'})
            tagas = content.find('ul',attrs={'class': 'list'}).find_all('a')
            for taga in tagas:
                try:
                    nowurl = urljoin(url,taga.get('href'))
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
            print('开始解析目标页面了\n')
            rep.encoding = 'utf-8'
            soup = BeautifulSoup(rep.text,'lxml')
            # print(soup)
            res = {}
            res['title'] = soup.find('div',attrs={'class':'con_wrap'}).find('h1').get_text()
            res['real_url'] = url
            # res['abstract'] = self.getContent(hrefurl)
            res['abstract'] = soup.find('div',attrs={'class':'content'}).get_text()
            res['time'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",soup.find('div', attrs={'class':'about'}).get_text()).group(0)
            res['site'] = '西藏人大网'
            # self.connection.insert(res)
            self.es.InsertData(res)
            # print(res)
        except Exception as e:
            print(e)
            print('西藏人大网')
            pass
    
    def run(self):
        for item_url in self.start_list:
            try:
                for i in range(30):
                    url = item_url.format(str(i))
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
    Spider = XizangSpider()
    Spider.run()
    # rep = Spider.crawl('http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')
    # Spider.parse(rep,'http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')



 