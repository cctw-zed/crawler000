from time import sleep
from bs4 import BeautifulSoup
import requests
# from ConOfAllData import ConOfAllData
from ES import ES

class HenanPeopleSpider(object):
    def __init__(self):
        # self.coad = ConOfAllData("henanrenda")
        # self.es = ES()
        self.es = ES('allspider')
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'www.henanrd.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        }

    def getPage(self, index_url):
        response = requests.get(index_url, headers=self.headers)
        if response.status_code == 200:
            response.encoding = "UTF-8"
            page = response.text
            self.parserPage(page)
            sleep(0.3)

    def parserPage(self, page):
        soup = BeautifulSoup(page, 'lxml')
        alist = soup.find("ul", attrs={'class': "list"})
        if alist is None:
            return
        else:
            alist = alist.findAll("li")
            print(len(alist))
            for item in alist:
                urlandtitle = item.find("a")
                real_url = urlandtitle.get("href")
                # if not self.coad.isexist(real_url):
                res = {}
                res["real_url"] = real_url
                res['title'] = urlandtitle.get_text()
                res['time'] = item.find("span").get_text()[1:11]
                res['site'] = "河南人大网"
                sleep(0.1)
                res['abstract'] = self.get_content(real_url)
                # print(res)
                self.es.InsertData(res)

    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response.encoding = "UTF-8"
            page = response.text
            soup = BeautifulSoup(page, 'lxml')
            abstract = soup.find("div", attrs={'class': "cl news-content"})
            abstract = abstract.get_text().strip()
            return abstract
        else:
            return None

    def run(self):
        url_list = [
            "https://www.henanrd.gov.cn/dflf/",
            "https://www.henanrd.gov.cn/jdgz/",
            "https://www.henanrd.gov.cn/xjrm/",
            "https://www.henanrd.gov.cn/jyjd/",
            "https://www.henanrd.gov.cn/dbgz/",
            "https://www.henanrd.gov.cn/jgjs/",
            "https://www.henanrd.gov.cn/rdyw/"
        ]
        for item in url_list:
            self.getPage(item)
        # self.coad.end()


if __name__ == "__main__":
    op = HenanPeopleSpider()
    op.run()
