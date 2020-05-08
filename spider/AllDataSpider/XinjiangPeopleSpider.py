from time import sleep
from bs4 import BeautifulSoup
import requests
import re
# from ConOfAllData import ConOfAllData
from ES import ES

class XinjiangPeopleSpider(object):
    def __init__(self):
        # self.coad = ConOfAllData("xinjiangrenda")
        # self.es = ES()
        self.es = ES('allspider')
        self.http_head = "http://www.xjpcsc.gov.cn"
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'www.xjpcsc.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        }

    def getPage(self, url_end):
        # 1 / jdsc.html
        url_head = "http://www.xjpcsc.gov.cn/channel/"
        page_index = 1
        while True:
            url = url_head + str(page_index) + url_end
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                page = response.text
                if not self.parserPage(page):
                    break
            page_index += 1
            sleep(0.3)

    def parserPage(self, page):
        soup = BeautifulSoup(page, 'lxml')
        alist = soup.find("ul", attrs={'class': "list"})
        alist = alist.findAll("li")
        print(alist)
        if len(alist) == 0:
            return False
        else:
            for item in alist:
                real_url = self.http_head + item.find("a").get("href")
                # if not self.coad.isexist(real_url):
                res = {}
                res["real_url"] = real_url
                res['title'] = item.find("a").get_text()
                if self.es.isExist(res['title']):
                    continue
                res['time'] = item.find("span").get_text()[1:11]
                res['site'] = '新疆人大网'
                sleep(0.1)
                res['abstract'] = self.get_content(real_url)
                # self.coad.insert(res)
                self.es.InsertData(res)
            return True

    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            page = response.text
            soup = BeautifulSoup(page, 'lxml')
            abstract = soup.find("div", attrs={"cl w1200"}).get_text().strip()
            if abstract == "":
                return None
            else:
                return abstract
        else:
            return None

    def run(self):
        url_end = [
            "/jggz.html",
            "/rdyw.html",
            "/lfgz.html",
            "/jdsc.html",
            "/dbhd.html",
            "/rsrm.html",
            "/zsxrd.html"
        ]
        for item in url_end:
            self.getPage(item)
        # self.coad.end()


if __name__ == "__main__":
    op = XinjiangPeopleSpider()
    op.run()
