from time import sleep
from bs4 import BeautifulSoup
from ConnectMongoDB import MyMongoDB
from ConnectToElasticSearch import ConnectToElasticSearch
import requests
import urllib.request
import time
from urllib.parse import urljoin
import re

class GuangdongSpider(object):
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
        self.seen = set()
        self.unseen = set([self.base_url, ])
        self.connection = ConnectToElasticSearch()

    # 抓取url得到response
    def crawl(self, url):
        # s = requests.session
        self.seen.add(url)
        self.unseen = self.unseen - self.seen
        try:
            response = requests.get(url,headers=self.headers)
            if response.status_code == 200:
                return response
        except:
            return False
    # 解析网页中包含的所有url
    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        urls = soup.find_all('a')
        page_urls = set()
        for url in urls:
            # title = url.get_text()
            url = url.get('href')
            print(url)
            full_url = urljoin(self.base_url, url)
            if 'html' in full_url:
                page_urls.add(full_url)
            else:
                self.unseen.add(full_url)
            # print(unseen)
        page_urls = page_urls - self.seen
        self.unseen = self.unseen - self.seen
        print('page_urls\n',page_urls)
        print('unseen\n',self.unseen)
        return page_urls


    def aimPageParse(self,rep, url):
        # print(contents_list)
        try:
            print('开始解析目标页面了')
            print(rep.encoding)
            rep.encoding = 'GBK'
            soup = BeautifulSoup(rep.text,'lxml')
            contents = soup.find('div', attrs={'class':'GtDetail'})
            # print(content)
            title = contents.find('div', attrs = {'class':'title'}).get_text()
            timegroup = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",contents.find('div', attrs={'class':'time'}).get_text())
            time = timegroup.group(0)
            content = contents.find('div', attrs={'class':'content'}).get_text().strip()
            res = {}
            res['title'] = title
            res['real_url'] = url
            # res['abstract'] = self.getContent(hrefurl)
            res['abstract'] = content
            res['time'] = time
            res['site'] = '广东人大网'
            # self.connection.insert(res)
            print(res)
        except:
            print('广东人大解析出错')
            pass
    
    def run(self):

        count, t1 = 1, time.time()

        while len(self.unseen) != 0:
            print('\nDistributed Crawling...')
            responses = []
            for url in self.unseen:
                responses.append(self.crawl(url))
                time.sleep(2)

            print('\nDistributed Parsing...')
            print(responses)
            print(self.unseen)
            for response in responses:
                try:
                    print('enter')
                    page_urls = self.parse(response)
                    for url in page_urls:
                        try:
                            rep = self.crawl(url)
                            if rep == False:
                                self.aimPageParse(rep, url)
                                time.sleep(2)
                                count += 1
                                print(count)                        
                            # print(time.time() - t1)
                        except:
                            continue
                except:
                    continue

        print('Total time: %.1f s' % (time.time() - t1,))  # 53 s

if __name__ == "__main__":
    Spider = GuangdongSpider()
    Spider.run()



 