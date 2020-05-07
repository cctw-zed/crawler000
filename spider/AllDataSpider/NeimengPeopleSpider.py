'''
1. 将需要爬取的文章列表页面放进待爬取列表
2. 对于每类页面，遍历
'''
import re
import time
from time import sleep
# from ConOfAllData import ConOfAllData
import requests
from bs4 import BeautifulSoup
from ES import ES

class NeimengPeopleSpider(object):

    def __init__(self):
        self.headers = {
            'Accept':'text/css,*/*;q=0.1',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'
        }
        # self.ConOfAllData("neimeng")
        self.baseUrl = 'http://www.nmgrd.gov.cn/'
        self.urlList_rightbox = {
            "xw/",  "jdgz/",
            "xjrm/", "sj2/",
            "jdsx/", "dfxfgzqyj/lfgzdd/",
        }
        # self.es = ES()
        self.es = ES('spider')

    def getResponse(self, urlList):
        # 对于列表中的所有url
        for url in urlList:
            fullUrl = self.baseUrl + url
            # print(fullUrl)
            # pages存放所有存放文章列表的页面
            pages = []
            firstPage = requests.get(fullUrl,headers=self.headers)
            if firstPage.status_code == 200:
                pages.append(firstPage)
            else:
                continue
            index = 1
            while True:
                sleep(0.3)
                tail = 'index_' + str(index) + '.html'
                try:
                    page = requests.get(fullUrl + tail)
                    # print(page)
                    if page.status_code == 200:
                        pages.append(page)
                        index += 1
                    else:
                        break;
                except:
                    break
            print('-----')
            self.parsePages(pages, fullUrl)

    def parsePages(self, pages, fullUrl):
        for page in pages:
            page.encoding = "utf-8"
            soup = BeautifulSoup(page.text, 'lxml')
            div = soup.find("div", {"class": "right_box"})
            if div == None:
                lists = soup.find_all('li', {'class': 'list hhh14'})
            else:
                lists = div.find_all('dl')
            for li in lists:
                # sleep(0.3)
                r = re.search(r'\./(.*?)html', str(li), re.M).group()[2:]
                articleUrl = fullUrl + r
                if re.match(r'\.\./(.*?)html', r):
                    r = r[3:]
                    articleUrl = self.baseUrl + r
                # if not self.ConOfAllData.isexist(articleUrl):
                # 注释部分用来按时间筛选
                # time_stamp_1 = time.mktime(time.strptime('2019-01-01', '%Y-%m-%d'))
                createdtime = li.find('span').get_text()
                # time_stamp_2 = time.mktime(time.strptime(createdtime, '%Y-%m-%d'))
                # if time_stamp_1 > time_stamp_2:
                #     continue
                res = {}
                p = self.parseArt(articleUrl)
                if p[1] == "":
                    continue
                res['title'] = p[1]
                res['real_url'] = articleUrl
                res['abstract'] = p[0]
                res['time'] = createdtime
                res['site'] = '内蒙古人大网'
                # print(res)
                self.es.InsertData(res)
                # self.ConOfAllData.insert(r
    def parseArt(self, articleUrl):
        try:
            response = requests.get(articleUrl,headers=self.headers)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, 'lxml')
            div = soup.find('div', attrs={'class':'TRS_Editor'})
            if div == None:
                div = soup.find('div', attrs={'class':'rd_wenzhang'})
            p = div.find('p')
            title = soup.find('div', attrs={'class':'content_title'})
            if title == None:
                title = soup.find('li', {'class':'lll24'})
            return p.get_text(), title.get_text()
        except:
            return "", ""

    def run(self):
        self.getResponse(self.urlList_rightbox)
        # self.ConOfAllData.end()

if __name__ == "__main__":
    spider = NeimengPeopleSpider()
    spider.run()
