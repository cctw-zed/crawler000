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

    def initSpiderList(self):
        self.spider_list.append(BeijingSpider(self.keyword))
        self.spider_list.append(AnhuiSpider(self.keyword))
        self.spider_list.append(ChinaPeopleSpider(self.keyword))
        self.spider_list.append(ChongqingSpider(self.keyword))
        self.spider_list.append(FujianPeopleSpider(self.keyword))
        
    
