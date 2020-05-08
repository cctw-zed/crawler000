import traceback
from flask import Flask, make_response
from time import sleep
from ES import ES
from flask_restful import reqparse, abort, Api, Resource
from BaiduSpider import BaiduSpider
from BeijingPeopleSpider import BeijingSpider
from ChinaPeopleSpider import ChinaPeopleSpider
from HubeiPeopleSpider import HubeiSpider
from HunanPeopleSpider import HunanSpider
from LiaoningPeopleSpider import LiaoNingPeopleSpider
from XinhuaSpider import XinhuaSpider
from AnhuiSpider import AnhuiSpider
from ChongqingSpider import ChongqingSpider
from FujianPeopleSpider import FujianPeopleSpider
from HeilongjiangSpider import HeilongjiangSpider
from JilinPeopleSpider import JilinSpider
from MountainWestSpider import MountainWestSpider
from QinghaiSpider import Qinghai
from ShandongSpider import ShandongSpider
from SichuanPeople import SichuanPeopleSpider
from HainanPeopleSpider import HainanPeopleSpider
from JiangxiPeopleSpider import JiangxiPeopleSpider
from GuangxiPeopleSpider import GuangxiPeopleSpider
from NingxiaPeopleSpider import NingxiaPeopleSpider

import threading

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


class my_easy_class(Resource):
    def post(self):
        args = parser.parse_args()
        keyword = args['keyword']

        # 爬虫
        baiduspider = BaiduSpider(keyword)
        beijingSpider = BeijingSpider(keyword)
        chinaSpider = ChinaPeopleSpider(keyword)
        hubeiSpider = HubeiSpider(keyword)
        hunanSpider = HunanSpider(keyword)
        liaoningSpider = LiaoNingPeopleSpider(keyword)
        xinhuaSpider = XinhuaSpider(keyword)
        anhuiSpider = AnhuiSpider(keyword)
        chongqingSpider = ChongqingSpider(keyword)
        fujianSpider = FujianPeopleSpider(keyword)
        heilongjiangSpider = HeilongjiangSpider(keyword)
        jilinSpider = JilinSpider(keyword)
        mountainWestSpider = MountainWestSpider(keyword)
        qinghaiSpider = Qinghai(keyword)
        shandongSpider = ShandongSpider(keyword)
        sichuanSpider = SichuanPeopleSpider(keyword)
        hainanSpider = HainanPeopleSpider(keyword)
        jiangxiSpider = JiangxiPeopleSpider(keyword)
        guangxiSpider = GuangxiPeopleSpider(keyword)
        ningxiaSpider = NingxiaPeopleSpider(keyword)

        thread_baidu = threading.Thread(target=baiduspider.run)
        thread_beijing = threading.Thread(target=beijingSpider.run)
        thread_china = threading.Thread(target=chinaSpider.run)
        thread_hubei = threading.Thread(target=hubeiSpider.run)
        thread_hunan = threading.Thread(target=hunanSpider.run)
        thread_liaoning = threading.Thread(target=liaoningSpider.run)
        thread_xinhua = threading.Thread(target=xinhuaSpider.run)
        thread_anhui = threading.Thread(target=anhuiSpider.run())
        thread_chongqing = threading.Thread(target=chongqingSpider.run())
        thread_fujian = threading.Thread(target=fujianSpider.run())
        thread_heilongjiang = threading.Thread(target=heilongjiangSpider.run())
        thread_jilin = threading.Thread(target=jilinSpider.run())
        thread_mountain = threading.Thread(target=mountainWestSpider.run())
        thread_qinghai = threading.Thread(target=qinghaiSpider.run())
        thread_shandong = threading.Thread(target=shandongSpider.run())
        thraed_sichuan = threading.Thread(target=sichuanSpider.run())
        thread_hainan = threading.Thread(target=hainanSpider.run())
        thread_jiangxi = threading.Thread(target=jiangxiSpider.run())
        thraed_guangxi = threading.Thread(target=guangxiSpider.run())
        thread_ningxia = threading.Thread(target=ningxiaSpider.run())

        thread_baidu.start()
        thread_beijing.start()
        thread_china.start()
        thread_hubei.start()
        thread_hunan.start()
        thread_liaoning.start()
        thread_xinhua.start()
        thread_anhui.start()
        thread_chongqing.start()
        thread_fujian.start()
        thread_heilongjiang.start()
        thread_jilin.start()
        thread_mountain.start()
        thread_qinghai.start()
        thread_shandong.start()
        thraed_sichuan.start()
        thread_hainan.start()
        thread_jiangxi.start()
        thraed_guangxi.start()
        thread_ningxia.start()

        op = {'re': 'it\'s working'}
        return op


class Sousuo:
    def __init__(self, keyword):
        self.keyword = keyword

    def run(self):
        sleep(20)
        workings.remove(self.keyword)


class Search(Resource):
    def __init__(self):
        self.es = ES('allspider')
        # 创建一个有搜索入口的es表

    def get(self):
        try:
            args = parser.parse_args()
            keyword = args['keyword']
            paramsppn = int(args['perPageNumber'])
            paramspi = int(args['pageIndex']) - 1
            # 除了全站的还需要补充有搜索入口的
            results = self.es.search([keyword])
            results = results["hits"]["hits"]
            # results_sousuo = self......
            # results_sousuo = results_sousuo["hits"]["hits"]
            # 合并两个数组  results和results_sousuo，最后结果是results
            length = len(results)
            if length == 0:
                re = {}
                re["success"] = False
                # 如果两个表都是空的，返回false，以便进行爬取
                return re
            else:
                re = {}
                re["success"] = True
                data = {}
                contentlist = []

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
                data["pageindex"] = paramspi
                data["totalnumber"] = length
                re["data"] = data

                # 控制一下，只有用户访问第一页时，才判断是否需要爬取
                # 如果用户点击下一页，不需要进行此语句
                if paramspi == 0:
                    if keyword not in workings:
                        workings.append(keyword)
                        # 启动搜索爬虫
                        sousuo = Sousuo(keyword)
                        thread_sousuo = threading.Thread(target=sousuo.run)
                        thread_sousuo.start()
                        print("有搜索结果，但是有搜索入口的需要爬取")
                    else:
                        print("有搜索结果，已经在爬取了，不要重复点击")
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
                    sousuo = Sousuo(keyword)
                    thread_sousuo = threading.Thread(target=sousuo.run)
                    thread_sousuo.start()
                    print("没有任何结果，启动带有搜索的爬虫")
                    re = {"feedback": "2"}
                else:
                    print("没有任何结果，带有搜索的爬虫已经在爬取了，不要重复点击")
                    re = {"feedback": "1"}
            response = make_response(re)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except:
            traceback.print_exc()


# 设置路由，即告诉Python程序URL的对应关系
# 类似 localhost:5000/my_easy_class.api
api.add_resource(my_easy_class, '/my_easy_class/api')
api.add_resource(Search, '/search/api')
api.add_resource(Canbegin, "/canbegin/api")

if __name__ == '__main__':
    app.run(debug=True)
