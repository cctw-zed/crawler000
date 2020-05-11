# from ConOfAllData import ConOfAllData
from time import sleep
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
from urllib.parse import urljoin
import re
from lxml import etree
from ES import ES

class HebeiPeopleSpider(object):
    def __init__(self):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        # self.connection = ConOfAllData('hebei')
        # self.es = ES()
        self.es = ES('allspider')

        self.start_list = [
            'http://www.hbrd.gov.cn/system/more/113002011000000000/0000/113002011000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113002001000000000/0000/113002001000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113003001000000000/0000/113003001000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113003003000000000/0000/113003003000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113003009000000000/0000/113003009000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113003006000000000/0000/113003006000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113006001000000000/0000/113006001000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113006004000000000/0000/113006004000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113006005000000000/0000/113006005000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113006007000000000/0000/113006007000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113012000000000000/0000/113012000000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113025000000000000/0000/113025000000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113022000000000000/0000/113022000000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113020000000000000/0000/113020000000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113004006000000000/0000/113004006000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113004010000000000/0000/113004010000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113004011000000000/0000/113004011000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113028000000000000/0000/113028000000000000_000000{}.shtml',
            'http://www.hbrd.gov.cn/system/more/113029000000000000/0000/113029000000000000_000000{}.shtml',
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
            html = BeautifulSoup(response.text, 'lxml')
            tagas = html.find('div', attrs ={'class':'m_list'}).find('ul').find_all('a')
      
            for taga in tagas:
                try:
                    nowurl = urljoin(url,taga.get('href'))
                    title = taga.get_text()
                    # if self.connection.isexist(nowurl)==False:
                    if self.es.isExist(title):
                        continue
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
            rep.encoding  = 'utf-8'
            soup = BeautifulSoup(rep.text,'lxml')
            # # print(soup)
            res = {}
            res['title'] = soup.find('div',attrs={'class':'title'}).get_text()
            res['real_url'] = url
            # res['abstract'] = self.getContent(hrefurl)
            res['abstract'] = soup.find('div',attrs={'class':'m_ct_txt'}).get_text().strip()
            res['time'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",soup.find('div', attrs={'class':'infobox'}).get_text()).group(0)[0:10]
            res['site'] = '河北人大网'
            # self.connection.insert(res)
            self.es.InsertData(res)
            # print(res)
        except Exception as e:
            print(e)
            print('河北人大网')
            pass
    
    def run(self):
        for item_url in self.start_list:
            try:
                for i in range(1,90):
                    if i > 10:
                        url = item_url.format(str(i))
                    else:
                        url = item_url.format( '0' + str(i))
                   
                    try:
                        # print(url)
                        rep = self.crawl(url)
                        if rep!=False and rep!=None:
                            self.parse(rep,url)
                    except:
                        continue
            except:
                continue
        # self.connection.end()
        

if __name__ == "__main__":
    Spider = HebeiPeopleSpider()
    Spider.run()
    # rep = Spider.crawl('http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')
    # Spider.parse(rep,'http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')



 