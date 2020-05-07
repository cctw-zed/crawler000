'''
1. 将需要爬取的文章列表页面放进待爬取列表
2. 对于每类页面，遍历
'''
from ES import ES
from time import sleep
# from ConOfAllData import ConOfAllData
import requests
from bs4 import BeautifulSoup

class YunnanPeopleSpider(object):

    def __init__(self):
        self.headers = {
            'Accept':'text/css,*/*;q=0.1',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'
        }
        # self.ConOfAllData("yunnan")
        # self.es = ES()
        self.es = ES('spider')
        self.baseUrl = 'http://www.srd.yn.gov.cn/'
        self.urlList = {
            'rdyw/',
            'ddjs/gzbs/', 'ddjs/xxdt/','ddjs/xxjy/',
            'zyfb/cwhgg/', 'zyfb/tzgs/','lfgz/lfdt/',
            'lfgz/syhd/', 'jdgz/gzjd/', 'jdgz/fljd/',
            'jdgz/ysjd/', 'jdgz/jhjd/', 'rsrm/',
            'dbgz/gzdt', 'dbgz/dbfc/', 'dbgz/xxpx',
            'ztjz/', 'jggz/jgjsgzdt/', 'jggz/jgjsxxpx/',
            'jggz/jggzfpgz/', 'jggz/bwcxljsm/', 'jggz/bwcxljsm/zybs/',
            'jggz/bwcxljsm/ynxd/', 'jggz/bwcxljsm/jgdt/', 'jggz/bwcxljsm/wlsp/',
            'gzyj/', 'fzxc/',
        }


    def getResponse(self):
        # 对于列表中的所有url
        for url in self.urlList:
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
                page = requests.get(fullUrl + tail)
                # print(page)
                if page.status_code == 200:
                    pages.append(page)
                    index += 1
                else:
                    break;
            # print('-----')
            self.parseResponse(pages,fullUrl)

    def parseResponse(self, pages, fullUrl):
        for page in pages:
            page.encoding = "utf-8"
            soup = BeautifulSoup(page.text, 'lxml')
            # print(soup)
            lis = soup.find('ul', attrs={'class':'newsline1'}).findAll('li')
            for li in lis:
                sleep(0.3)
                a = li.find('a')
                articleUrl = fullUrl + a['href'][2:]
                # if not self.ConOfAllData.isexist(articleUrl):
                res = {}
                res['title'] = a.get_text()
                res['real_url'] = articleUrl
                res['abstract'] = self.parseArt(articleUrl)
                res['time'] = li.find('span').get_text()
                res['site'] = '云南人大网'
                self.es.InsertData(res)

                # print(res)
                    # self.ConOfAllData.insert(res)

    def parseArt(self, articleUrl):
        response = requests.get(articleUrl,headers=self.headers)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            div = soup.find('div', attrs={'class':'TRS_Editor'})
            p = div.find('p')
            return p.get_text()
        except:
            return ""

    def run(self):
        self.getResponse()
        # self.ConOfAllData.end()

if __name__ == "__main__":
    spider = YunnanPeopleSpider()
    spider.run()
