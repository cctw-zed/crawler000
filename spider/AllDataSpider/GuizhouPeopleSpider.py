from time import sleep
from bs4 import BeautifulSoup
import requests
import re
# from ConOfAllData import ConOfAllData
# from ES import ES

class GuizhouPeopleSpider(object):
    def __init__(self):
        # self.coad = ConOfAllData("guizhourenda")
        self.es = ES()
        self.http_head = "http://www.gzrd.gov.cn"
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'www.gzrd.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        }

    def getPage(self, url_head):
        url = url_head + "index.shtml"
        response = requests.get(url, headers=self.headers)
        page_index = 2
        while response.status_code == 200:
            response.encoding = "UTF-8"
            page = response.text
            self.parserPage(page)
            url = url_head + "index_" + str(page_index) + ".shtml"
            page_index += 1
            sleep(0.5)
            response = requests.get(url, headers=self.headers)

    def parserPage(self, page):
        soup = BeautifulSoup(page, 'lxml')
        alist = soup.find("div", attrs={'class': "list-box"})
        if alist is None:
            return
        alist = alist.findAll("li")
        print(len(alist))
        for item in alist:
            hrefandtitle = item.find("a")
            real_url = self.http_head + hrefandtitle.get("href")
            # if not self.coad.isexist(real_url):
            res = {}
            res["real_url"] = real_url
            res['title'] = hrefandtitle.get("title")
            res['time'] = item.find("span").get_text()
            res['site'] = '贵州人大网'
            sleep(0.1)
            res['abstract'] = self.get_content(real_url)
            self.es.InsertData(res)

    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        response.encoding = "UTF-8"
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        abstracts = soup.find("div", attrs={'class': "view"})
        abstracts = abstracts.findAll('p')
        abstract = ""
        for item in abstracts:
            content_eve = item.get_text().strip()
            if content_eve != "":
                abstract += item.get_text().strip() + "\n"
        if abstract == "":
            return None
        else:
            return abstract

    def run(self):
        url_head = [
            "http://www.gzrd.gov.cn/rdgl/bjdbdhgk/",
            "http://www.gzrd.gov.cn/rdgl/ljdbdhgk/",
            "http://www.gzrd.gov.cn/xwzx/zyfb/dbdhgg/",
            "http://www.gzrd.gov.cn/xwzx/zyfb/cwhgg/",
            "http://www.gzrd.gov.cn/xwzx/zyfb/jyjd/",
            "http://www.gzrd.gov.cn/xwzx/zyfb/tzgg/",
            "http://www.gzrd.gov.cn/gzdt/lfgz/lfjj/",
            "http://www.gzrd.gov.cn/gzdt/lfgz/lfgs/",
            "http://www.gzrd.gov.cn/gzdt/lfgz/wnlfgh/",
            "http://www.gzrd.gov.cn/gzdt/lfgz/ndlfjh/",
            "http://www.gzrd.gov.cn/gzdt/jdgz/zfjc/",
            "http://www.gzrd.gov.cn/gzdt/jdgz/tqsybg/",
            "http://www.gzrd.gov.cn/gzdt/jdgz/ztxw/",
            "http://www.gzrd.gov.cn/gzdt/jdgz/zhbd/",
            "http://www.gzrd.gov.cn/gzdt/dbgz/dbfc/",
            "http://www.gzrd.gov.cn/gzdt/dbgz/lzdt/",
            "http://www.gzrd.gov.cn/gzdt/dbgz/yajy/",
            "http://www.gzrd.gov.cn/gzdt/dbgz/dbzgsc/",
            "http://www.gzrd.gov.cn/gzdt/dbgz/zhbd/",
            "http://www.gzrd.gov.cn/gzdt/xjrm/",
            "http://www.gzrd.gov.cn/gzdt/jggz/dj1/",
            "http://www.gzrd.gov.cn/gzdt/jggz/jgxx/",
            "http://www.gzrd.gov.cn/gzdt/jggz/sgjfs/",
            "http://www.gzrd.gov.cn/dffg/gzsdffg/",
            "http://www.gzrd.gov.cn/dffg/szdffg/",
            "http://www.gzrd.gov.cn/dffg/zztldxtl/"
        ]
        for item in url_head:
            self.getPage(item)
        # self.coad.end()


if __name__ == "__main__":
    op = GuizhouPeopleSpider()
    op.run()
