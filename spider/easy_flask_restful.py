from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from spiders.BaiduSpider import BaiduSpider
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
        sp = BaiduSpider(keyword)
        thread_hi = threading.Thread(target=sp.run)
        thread_hi.start()

        op = {'re': 'it\'s working'}
        return op

# 设置路由，即告诉Python程序URL的对应关系
# 类似 localhost:5000/my_easy_class.api
api.add_resource(my_easy_class, '/my_easy_class/api')

if __name__ == '__main__':
    app.run(debug=True)