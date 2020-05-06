'''
1. 将需要爬取的文章列表页面放进待爬取列表
2. 对于每类页面，遍历
'''
from time import sleep
from ConOfAllData import ConOfAllData
import requests
from bs4 import BeautifulSoup

class ZheJiangSpider(object):

    def __init__(self):
        self.headers = {
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate',
           'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'
        }
        self.ConOfAllData("zhejiang")
        self.baseUrl = 'http://www.zjrd.gov.cn/'
        self.urlList = {
            'rdgl/gzzd/','rdgl/rdzs/',
            'zyfb/cwhgg/','zyfb/jyjd/','zyfb/tzgg/','zyfb/yjsgk/',
            'dflf/lfzt/','dflf/fggg','dflf/hysy/','dflf/lfdy/','dflf/yjzj/','dflf/lfjy/',
            'jdgj/jdzt/','jdgj/gzjd/','jdgj/sfjd/','jdgj/fljd/','jdgj/ysjd/',
            'xjrm/rd/','xjrm/zf/','xjrm/jcw/','xjrm/fy/','xjrm/jcy/',
            'dbgz/dbhd/','dbgz/dblz/','dbgz/jybl/','dbgz/xxpx/',
            'sxrd/hzs/','sxrd/nbs/','sxrd/wzs/','sxrd/hzs/','sxrd/jxs/','sxrd/sxs/','sxrd/jhs/','sxrd/qzs/','sxrd/zss/','sxrd/tzs/','sxrd/lss/',
            'jgjs/jgdt/','jgjs/xxjz/','jgjs/dwjl/',
            'llyj/sndt/','llyj/srdcg/',
            'mtgz/',
            'rdh/lcrdh/','cwh/lccwh/',
        }


    def getResponse(self):
        # 对于列表中的所有url
        for url in self.urlList:
            fullUrl = self.baseUrl + url
            # pages存放所有存放文章列表的页面
            pages = []
            pages.append(requests.get(fullUrl,headers=self.headers))
            index = 1
            while True:
                sleep(0.3)
                tail = 'index_' + str(index) + '.html'
                page = requests.get(fullUrl + tail)
                if page.status_code == 200:
                    pages.append(page)
                    index += 1
                else:
                    break;
            self.parseResponse(pages,fullUrl)

    def parseResponse(self, pages, fullUrl):
        for page in pages:
            soup = BeautifulSoup(page.text, 'lxml')
            tables = soup.findAll('table', attrs={'width':'770'})
            for table in tables:
                sleep(0.3)
                a = table.find('a')
                articleUrl = fullUrl+a['href'][2:]
                if not self.ConOfAllData.isexist(articleUrl):
                    res = {}
                    res['title'] = a.get_text()
                    res['real_url'] = articleUrl
                    res['abstract'] = self.parseArt(articleUrl)
                    res['time'] = table.find('td', attrs={'width':'12%'}).get_text()
                    res['site'] = '浙江人大网'
                    print(res)
                    self.ConOfAllData.insert(res)

    def parseArt(self, articleUrl):
        response = requests.get(articleUrl,headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find('div', attrs={'class':'TRS_Editor'})
        p = div.find('p')
        return p.get_text()

    def run(self):
        try:
            self.getResponse()
            self.ConOfAllData.end()
        except:
            print("失败")

if __name__ == "__main__":
    spider = ZheJiangSpider()
    spider.run()
