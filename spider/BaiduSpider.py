import urllib
from time import sleep
from ConnectMongoDB import MyMongoDB
import requests
from bs4 import BeautifulSoup

class BaiduSpider(object):

    def __init__(self, keyword):
        self.keyword = keyword
        self.connection = MyMongoDB()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'BIDUPSID=EEE9FED806AEBDF27D8BD1F68FDE2758; PSTM=1572065115; BAIDUID=EEE9FED806AEBDF24ED0F7EBBC77417E:FG=1; BD_UPN=12314753; BDUSS=k4dEVuN3NLdmZ2V3loeElNR000WjRyVUpuVWR2T2hJYW50YXNOYkpVSnFiSkZlRVFBQUFBJCQAAAAAAAAAAAEAAAC2538~U2lsdmVyx7OzwQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGrfaV5q32leZm; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; ZD_ENTRY=empty; delPer=0; BD_CK_SAM=1; PSINO=7; BDRCVFR[VXHUG3ZuJnT]=mk3SLVN4HKm; sug=3; sugstore=0; ORIGIN=2; bdime=0; H_PS_645EC=476a2vjcYBLh9uWLj%2B%2BSkgD1TGPVaJZvs42JeM76S0jjojq7r9AKzi5FB6952%2BGkAlq36NfhRyZK; BDSVRTM=95',
            'Host': 'www.baidu.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.sitelist = [
            ['新华网', 'xinhuanet.com'],
            ['人民网', 'people.com.cn'],
            ['搜狐网', 'sohu.com'],
            ['凤凰网', 'ifeng.com'],
            ['新浪网', 'sina.com'],
            ['腾讯网', 'qq.com'],
            # ['中国人大网','npc.gov.cn'],
            # ['北京人大网','bjrd.gov.cn']
        ]


    def parse(self, response, keyword, site):
        # page = response.read().decode('utf-8')
        page = response.text
        soup = BeautifulSoup(page)
        # print(soup)
        # print(page)
        divs = soup.find_all('div', attrs={"class": 'result c-container'})
        # print(divs)
        reslist = []
        for div in divs:
            try:
                contentdiv = div.find('div')
                abstract = contentdiv.text
                time = div.find('span').text
                h3 = div.find('h3')
                taga = h3.find('a')
                href = taga.get('href')
                title = taga.text
                baidu_url = requests.get(url=href, headers= self.headers, allow_redirects=False)
                real_url = baidu_url.headers['Location']  # 得到网页原始地址
                if real_url.startswith('http'):
                    res = {}
                    res['title'] = title
                    res['time'] = time.replace('-', '').replace(' ', '')
                    res['real_url'] = real_url
                    res['abstract'] = abstract
                    res['keyword'] = keyword
                    res['site'] = site[0]
                    # 放进数据库
                    self.connection.insert(res)
                    reslist.append(res)
            except:
                continue
        return reslist

    def getContent(self, keyword, pageIndex, site):
        url = 'https://www.baidu.com/s?wd=' + urllib.parse.quote(keyword + ' ') + 'site:' + site[1] + '&pn=' + str(
            (pageIndex - 1) * 10)
        # url2 = 'https://www.baidu.com/s?wd=疫情%20site%3Axinhuanet.com&pn=30'
        response = requests.get(url = url, headers = self.headers)
        if response.status_code == 200:
            return self.parse(response, keyword, site)

        else:
            return ''

    def run(self):
        # print("run begin!")
        for i in range(len(self.sitelist)):
            site = self.sitelist[i]
            for j in range(3):
                sleep(1)
                res = self.getContent(self.keyword, j + 1, site)
                #print(res)
        print("sasss")
        self.connection.deleteKeyword(self.keyword)
        
