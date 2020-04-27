from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED
from BeijingPeopleSpider import BeijingSpider
from AnhuiSpider import AnhuiSpider
from ChinaPeopleSpider import ChinaPeopleSpider
from ChongqingSpider import ChongqingSpider
from FujianPeopleSpider import FujianPeopleSpider
from HainanPeopleSpider import HainanPeopleSpider
from HeilongjiangSpider import HeilongjiangSpider
from HubeiPeopleSpider import HubeiSpider
from HunanPeopleSpider import HunanSpider
from JilinPeopleSpider import JilinSpider
from LiaoningPeopleSpider import LiaoNingPeopleSpider
from MountainWestSpider import MountainWestSpider
from ShandongSpider import ShandongSpider
from SichuanPeople import SichuanPeopleSpider
from SinaSpider import SinaSpider
from XinhuaSpider import XinhuaSpider


class SpiderManager(object):
    def __init__(self,keyword):
        self.keyword = keyword
        self.spider_list = []
        self.initSpiderList()

    def initSpiderList(self):
        self.spider_list.append(BeijingSpider(self.keyword))
        # self.spider_list.append(AnhuiSpider(self.keyword))
        self.spider_list.append(ChinaPeopleSpider(self.keyword))
        self.spider_list.append(ChongqingSpider(self.keyword))
        self.spider_list.append(FujianPeopleSpider(self.keyword))
        self.spider_list.append(HainanPeopleSpider(self.keyword))
        # self.spider_list.append(HeilongjiangSpider(self.keyword))
        self.spider_list.append(HubeiSpider(self.keyword))
        self.spider_list.append(HunanSpider(self.keyword))
        self.spider_list.append(JilinSpider(self.keyword))
        self.spider_list.append(LiaoNingPeopleSpider(self.keyword))
        self.spider_list.append(MountainWestSpider(self.keyword))
        self.spider_list.append(ShandongSpider(self.keyword))
        self.spider_list.append(SichuanPeopleSpider(self.keyword))
        self.spider_list.append(SinaSpider(self.keyword))
        self.spider_list.append(XinhuaSpider(self.keyword))
    
    def run(self):
        with ThreadPoolExecutor(max_workers=5) as t:
            for spider in self.spider_list:
                t.submit(spider.run)

if __name__ == "__main__":
    spider = SpiderManager('疫情')
    spider.run()


    
