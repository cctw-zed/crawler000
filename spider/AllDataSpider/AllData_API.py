import traceback
from flask import Flask, make_response
from time import sleep
from ES import ES
from flask_restful import reqparse, abort, Api, Resource
import threading

import sys
sys.path.append("..")
from AnhuiSpider import AnhuiSpider
from BaiduSpider import BaiduSpider
from BeijingPeopleSpider import BeijingSpider
from ChinaPeopleSpider import ChinaPeopleSpider
from ChongqingSpider import ChongqingSpider
from FujianPeopleSpider import FujianPeopleSpider
from GuangxiPeopleSpider import GuangxiPeopleSpider
from HainanPeopleSpider import HainanPeopleSpider
from HeilongjiangSpider import HeilongjiangSpider
from HubeiPeopleSpider import HubeiSpider
from HunanPeopleSpider import HunanSpider
from JiangxiPeopleSpider import JiangxiPeopleSpider
from JilinPeopleSpider import JilinSpider
from LiaoningPeopleSpider import LiaoNingPeopleSpider
from MountainWestSpider import MountainWestSpider
from NingxiaPeopleSpider import NingxiaPeopleSpider
from QinghaiSpider import Qinghai
from ShandongSpider import ShandongSpider
from ShanghaiSpider import ShanghaiSpider
from SichuanPeople import SichuanPeopleSpider
from SinaSpider import SinaSpider
from XinhuaSpider import XinhuaSpider


# 做简单的Application初始化
app = Flask(__name__)
api = Api(app)  # 用Api来绑定app

# 参数解析的RequestParser类，可以很方便的解析请求中的-d参数，并进行类型转换
parser = reqparse.RequestParser()
# parser.add_argument('task')
parser.add_argument('keyword')
parser.add_argument('perPageNumber')
parser.add_argument('pageIndex')
parser.add_argument('captcha')

workings = []


class KeywordSearch:
    def __init__(self, keyword):
        self.keyword = keyword

    def run(self):
        anhui = AnhuiSpider(self.keyword)
        baidu = BaiduSpider(self.keyword)
        beijing = BeijingSpider(self.keyword)
        china = ChinaPeopleSpider(self.keyword)
        chongqing = ChongqingSpider(self.keyword)
        fujian = FujianPeopleSpider(self.keyword)
        guangxi = GuangxiPeopleSpider(self.keyword)
        hainan = HainanPeopleSpider(self.keyword)
        heilongjiang = HeilongjiangSpider(self.keyword)
        hubei = HubeiSpider(self.keyword)
        hunan = HunanSpider(self.keyword)
        jiangxi = JiangxiPeopleSpider(self.keyword)
        jiling = JilinSpider(self.keyword)
        liaoning = LiaoNingPeopleSpider(self.keyword)
        mountain = MountainWestSpider(self.keyword)
        ningxia = NingxiaPeopleSpider(self.keyword)
        qinghai = Qinghai(self.keyword)
        shandong = ShandongSpider(self.keyword)
        shanghai = ShanghaiSpider(self.keyword)
        sichuan = SichuanPeopleSpider(self.keyword)
        sina = SinaSpider(self.keyword)
        xinhua = XinhuaSpider(self.keyword)

        threadlist = []
        thread_anhui = threading.Thread(target=anhui.run)
        threadlist.append(thread_anhui)
        thread_baidu = threading.Thread(target=baidu.run)
        threadlist.append(thread_baidu)
        thread_beijing = threading.Thread(target=beijing.run)
        threadlist.append(thread_beijing)
        thread_china = threading.Thread(target=china.run)
        threadlist.append(thread_china)
        thread_chongqing = threading.Thread(target=chongqing.run)
        threadlist.append(thread_chongqing)
        thread_fujian = threading.Thread(target=fujian.run)
        threadlist.append(thread_fujian)
        thread_guangxi = threading.Thread(target=guangxi.run)
        threadlist.append(thread_guangxi)
        thread_hainan = threading.Thread(target=hainan.run)
        threadlist.append(thread_hainan)
        thread_heilongjiang = threading.Thread(target=heilongjiang.run)
        threadlist.append(thread_heilongjiang)
        thread_hubei = threading.Thread(target=hubei.run)
        threadlist.append(thread_hubei)
        thread_hunan = threading.Thread(target=hunan.run)
        threadlist.append(thread_hunan)
        thread_jiangxi = threading.Thread(target=jiangxi.run)
        threadlist.append(thread_jiangxi)
        thread_jiling = threading.Thread(target=jiling.run)
        threadlist.append(thread_jiling)
        thread_liaoning = threading.Thread(target=liaoning.run)
        threadlist.append(thread_liaoning)
        thread_mountain = threading.Thread(target=mountain.run)
        threadlist.append(thread_mountain)
        thread_ningxia = threading.Thread(target=ningxia.run)
        threadlist.append(thread_ningxia)
        thread_qinghai = threading.Thread(target=qinghai.run)
        threadlist.append(thread_qinghai)
        thread_shandong = threading.Thread(target=shandong.run)
        threadlist.append(thread_shandong)
        thread_shanghai = threading.Thread(target=shanghai.run)
        threadlist.append(thread_shanghai)
        thread_sichuan = threading.Thread(target=sichuan.run)
        threadlist.append(thread_sichuan)
        thread_sina = threading.Thread(target=sina.run)
        threadlist.append(thread_sina)
        thread_xinhua = threading.Thread(target=xinhua.run)
        threadlist.append(thread_xinhua)
        # thread_anhui.start()
        # thread_baidu.start()
        # thread_beijing.start()
        # thread_china.start()
        # thread_chongqing.start()
        # thread_fujian.start()
        # thread_guangxi.start()
        # thread_hainan.start()
        # thread_heilongjiang.start()
        # thread_hubei.start()
        # thread_hunan.start()
        # thread_jiangxi.start()
        # thread_jiling.start()
        # thread_liaoning.start()
        # thread_mountain.start()
        # thread_ningxia.start()
        # thread_qinghai.start()
        # thread_shandong.start()
        # thread_shanghai.start()
        # thread_sichuan.start()
        # thread_sina.start()
        # thread_xinhua.start()
        for item in threadlist:
            item.start()
        for item in threadlist:
            item.join()
        workings.remove(self.keyword)
        print("完成")

class Search(Resource):
    def __init__(self):
        self.es = ES('allspider')
        # 创建一个有搜索入口的es表
        self.prees = ES('prespider')

    def get(self):
        try:
            args = parser.parse_args()
            keyword = args['keyword']
            paramsppn = int(args['perPageNumber'])
            paramspi = int(args['pageIndex']) - 1
            # 除了全站的还需要补充有搜索入口的
            results = self.es.search([keyword])
            results = results["hits"]["hits"]
            # 关键字
            pre_results = self.prees.search([keyword])
            pre_results = pre_results["hits"]["hits"]
            length = len(pre_results)
            if length == 0:
                re = {}
                re["success"] = False
                response = make_response(re)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                re = {}
                re["success"] = True
                data = {}
                contentlist = []

                # 合并两个数组，结果用result表示
                results.extend(pre_results)
                results.sort(key=lambda x: x["_score"], reverse=True)

                need_results = results[paramspi * paramsppn:(paramspi + 1) * paramsppn]
                for item in need_results:
                    need_content = {}
                    need_content["content"] = item["_source"]["abstract"]
                    need_content["title"] = item["_source"]["title"]
                    need_content["time"] = item["_source"]["time"]
                    need_content["url"] = item["_source"]["real_url"]
                    need_content["platform"] = item["_source"]["site"]
                    contentlist.append(need_content)

                data["contentlist"] = contentlist
                data["pageindex"] = paramspi + 1
                data["totalnumber"] = len(results)
                re["data"] = data
                response = make_response(re)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
        except:
            traceback.print_exc()


class Canbegin(Resource):
    def get(self):
        try:
            args = parser.parse_args()
            keyword = args['keyword']
            captcha = args['captcha']
            if captcha != "search":
                re = {"feedback": "0"}
            else:
                if keyword not in workings:
                    workings.append(keyword)
                    # 启动搜索爬虫
                    keywordsearch = KeywordSearch(keyword)
                    thread_keywordsearch = threading.Thread(target=keywordsearch.run)
                    thread_keywordsearch.start()
                    print("开始爬取")
                    re = {"feedback": "2"}
                else:
                    print(workings)
                    print("已经在爬取了")
                    re = {"feedback": "1"}
            response = make_response(re)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except:
            traceback.print_exc()


# 设置路由，即告诉Python程序URL的对应关系
# 类似 localhost:5000/my_easy_class.api
api.add_resource(Search, '/api/search')
api.add_resource(Canbegin, "/api/canbegin")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
