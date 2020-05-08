# from ConOfAllData import ConOfAllData
from time import sleep
from ES import ES
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
from urllib.parse import urljoin
import re
from lxml import etree

class TianJinSpider(object):
    def __init__(self):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        # self.connection = ConOfAllData('tianjin')
        # self.es = ES()
        self.es = ES('allspider')
        self.start_list = [
            'http://www.tjrd.gov.cn/xwzx/system/count//0003016/000000000000/000/000/c0003016000000000000_0000000{}.shtml',
            'http://www.tjrd.gov.cn/xwzx/system/count//0003001/000000000000/000/000/c0003001000000000000_0000000{}.shtml',
            'http://www.tjrd.gov.cn/xwzx/system/count//0003003/000000000000/000/000/c0003003000000000000_0000000{}.shtml',
            'http://www.tjrd.gov.cn/xwzx/system/count//0003015/000000000000/000/000/c0003015000000000000_0000000{}.shtml',
            'http://www.tjrd.gov.cn/xwzx/system/count//0003014/000000000000/000/000/c0003014000000000000_0000000{}.shtml',
            'http://www.tjrd.gov.cn/xwzx/system/count//0003010/000000000000/000/000/c0003010000000000000_0000000{}.shtml',
            'http://www.tjrd.gov.cn/xwzx/system/count//0003010/001000000000/000/000/c0003010001000000000_0000000{}.shtml',
            'http://www.tjrd.gov.cn/xwzx/system/count//0003010/002000000000/000/000/c0003010002000000000_0000000{}.shtml',
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
            tagas = html.find_all('td', attrs= {'class': 'weiruan16 hanggao36', 'width':'77%', 'align':'left'})
      
            for taga in tagas:
                try:
                    nowurl = urljoin(url,taga.find('a').get('href'))
                    title = taga.find('a').get_text()
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
            rep.encoding  = 'gb2312'
            soup = BeautifulSoup(rep.text,'lxml')
            # # print(soup)
            res = {}
            res['title'] = soup.find('td',attrs={'class':'weiruan30'}).get_text()
            res['real_url'] = url
            # res['abstract'] = self.getContent(hrefurl)
            res['abstract'] = soup.find('td',attrs={'class':'hanggao36 weiruan16'}).get_text().strip()
            res['time'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",soup.find('td', attrs={'class':'weiruan zi14'}).get_text()).group(0)[0:10]
            res['site'] = '天津人大网'
            # self.connection.insert(res)
            self.es.InsertData(res)
            # print(res)
        except Exception as e:
            print(e)
            print('天津人大网')
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
                        print(url)
                        rep = self.crawl(url)
                        if rep!=False and rep!=None:
                            self.parse(rep,url)
                    except:
                        continue
            except:
                continue
        # self.connection.end()
        

if __name__ == "__main__":
    Spider = TianJinSpider()
    Spider.run()
    # rep = Spider.crawl('http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')
    # Spider.parse(rep,'http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')



 