# from ConOfAllData import ConOfAllData
from ES import ES
from time import sleep
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
from urllib.parse import urljoin
import re

class GuangdongPeopleSpider(object):
    def __init__(self):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

        self.base_url = 'http://www.rd.gd.cn/'
        # self.connection = ConOfAllData('guangdong')
        self.es = ES()
        self.start_list = [
            'http://www.rd.gd.cn/pub/gdrd2012/rdgz/lfjj/',
            'http://www.rd.gd.cn/pub/gdrd2012/rdgz/jdsd',
            'http://www.rd.gd.cn/pub/gdrd2012/rdhy/jyjd/',
            'http://www.rd.gd.cn/pub/gdrd2012/rdhy/rsrm/',
            'http://www.rd.gd.cn/pub/gdrd2012/dbgz/',
            'http://www.rd.gd.cn/pub/gdrd2012/xxgk/',
            'http://www.rd.gd.cn/pub/gdrd2012/zsjs/',
            'http://www.rd.gd.cn/pub/gdrd2012/gzjl/dwjw/',
            'http://www.rd.gd.cn/pub/gdrd2012/rdgz/gsrd/',
            'http://www.rd.gd.cn/pub/gdrd2012/yfzs/fzxc/',
            'http://www.rd.gd.cn/pub/gdrd2012/rdyj/rdlt/',
            'http://www.rd.gd.cn/pub/gdrd2012/xwsc/rdxw/',
            'http://www.rd.gd.cn/pub/gdrd2012/xwzc/tpxw/',
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
            response.encoding = 'GBK'
            soup = BeautifulSoup(response.text)
            uls = soup.find_all('ul',attrs={'class': 'GsTL1 nesadd'})
            if len(uls)==0:
                uls = soup.find_all('ul', attrs={'class':'GsTL1'})
            for ul in uls:
                tagas = ul.find_all('a')
                for taga in tagas:
                    try:
                        nowurl = urljoin(url,taga.get('href'))
                        # if self.connection.isexist(nowurl)==False:
                        rep = self.crawl(nowurl)
                        self.aimPageParse(rep,nowurl)
                    except:
                        continue
        except:
            print('解析栏目链接出错')
            pass


    def aimPageParse(self,rep, url):
        # print(contents_list)
        try:
            # print('开始解析目标页面了\n')
            rep.encoding = 'GBK'
            soup = BeautifulSoup(rep.text,'lxml')
            contents = soup.find('div', attrs={'class':'GtDetail'})
            # print(content)
            title = contents.find('div', attrs = {'class':'title'}).get_text()
            timegroup = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",contents.find('div', attrs={'class':'time'}).get_text())
            createdtime = timegroup.group(0)[0:10]
            content = contents.find('div', attrs={'class':'content'}).get_text().strip()
            res = {}
            res['title'] = title
            res['real_url'] = url
            # res['abstract'] = self.getContent(hrefurl)
            res['abstract'] = content
            res['time'] = createdtime
            res['site'] = '广东人大网'
            # self.connection.insert(res)
            self.es.InsertData(res)
            # print(res)
        except:
            print('广东人大解析出错')
            pass
    
    def run(self):
        for item_url in self.start_list:
            try:
                for i in range(10):
                    if i==0:
                        url = urljoin(item_url, 'index.html')
                    else:
                        url = urljoin(item_url,'index_'+str(i)+'.html')
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
    Spider = GuangdongPeopleSpider()
    Spider.run()
    # rep = Spider.crawl('http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')
    # Spider.parse(rep,'http://www.rd.gd.cn/pub/gdrd2012/rdzs/index.html')



 