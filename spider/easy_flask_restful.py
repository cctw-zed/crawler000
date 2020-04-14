from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from BaiduSpider import BaiduSpider
from BeijingPeopleSpider import BeijingSpider
from ChinaPeopleSpider import ChinaPeopleSpider
from HuBeiPeopleSpider import HuBeiSpider
from HunanPeopleSpider import HunanSpider
from LiaoningPeopleSpider import LiaoNingPeopleSpider
from XinhuaSpider import XinhuaSpider
import threading

# 做简单的Application初始化
app = Flask(__name__)
api = Api(app)  # 用Api来绑定app

# 参数解析的RequestParser类，可以很方便的解析请求中的-d参数，并进行类型转换
parser = reqparse.RequestParser()
# parser.add_argument('task')
parser.add_argument('keyword')

class my_easy_class(Resource):
    def post(self):
        args = parser.parse_args()
        keyword = args['keyword']

        #爬虫
        baiduspider = BaiduSpider(keyword)
        beijingSpider = BeijingSpider(keyword)
        chinaSpider = ChinaPeopleSpider(keyword)
        hubeiSpider = HuBeiSpider(keyword)
        hunanSpider = HunanSpider(keyword)
        liaoningSpider = LiaoNingPeopleSpider(keyword)
        xinhuaSpider  = XinhuaSpider(keyword)

        thread_baidu = threading.Thread(target=baiduspider.run)
        thread_beijing = threading.Thread(target=beijingSpider.run)
        thread_china = threading.Thread(target=chinaSpider.run)
        thread_hubei = threading.Thread(target=hubeiSpider.run)
        thread_hunan = threading.Thread(target=hunanSpider.run)
        thread_liaoning = threading.Thread(target=liaoningSpider.run)
        thread_xinhua = threading.Thread(target=xinhuaSpider.run)
         
        thread_baidu.start()
        thread_beijing.start()
        thread_china.start()
        thread_hubei.start()
        thread_hunan.start()
        thread_liaoning.start()
        thread_xinhua.start()

        op = {'re': 'it\'s working'}
        return op

# 设置路由，即告诉Python程序URL的对应关系
# 类似 localhost:5000/my_easy_class.api
api.add_resource(my_easy_class, '/my_easy_class/api')

if __name__ == '__main__':
    app.run(debug=True)
