from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from Connect_MongoDB import MyMongoDB
from spders.BaiduSpider import BaiduSpider
import threading

# 做简单的Application初始化
app = Flask(__name__)
api = Api(app)  # 用Api来绑定app

# 定义我们需要操作的资源类型（都是json格式的）
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈'},
    'todo3': {'task': 'profit!'},
}


# 验证todo_id是否在TODOS当中
def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


# 参数解析的RequestParser类，可以很方便的解析请求中的-d参数，并进行类型转换
parser = reqparse.RequestParser()
# parser.add_argument('task')
parser.add_argument('keyword')


# 操作（put / get / delete）单一资源Todo
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)  # 进行请求前，先做id确认
        return TODOS[todo_id]  # 从TODOS字典中读取数据

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# # 操作（post / get）资源列表TodoList
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

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
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(my_easy_class, '/my_easy_class/api')

if __name__ == '__main__':
    app.run(debug=True)