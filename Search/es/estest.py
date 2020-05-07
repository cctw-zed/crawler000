import json

from elasticsearch import Elasticsearch

es = Elasticsearch()
mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}
# result = es.indices.delete(index='my_index', ignore=[400, 404])
# print(result)
# es.indices.create(index='news', ignore=400)
# result = es.indices.put_mapping(index='news', body=mapping)
# print(result)

# datas = [
#     {
#         'title': '美国留给伊拉克的是个烂摊子吗',
#         'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
#         'date': '2011-12-16'
#     },
#     {
#         'title': '公安部：各地校车将享最高路权',
#         'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
#         'date': '2011-12-16'
#     },
#     {
#         'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
#         'url': 'https://news.qq.com/a/20111216/001044.htm',
#         'date': '2011-12-17'
#     },
#     {
#         'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
#         'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
#         'date': '2011-12-18'
#     }
# ]
#
# for data in datas:
#     es.index(index='news', body=data)

# result = es.search(index='news')
# print(result)
#
# dsl = {
#     'query': {
#         'match': {
#             'title': '中国 领事馆'
#         }
#     }
# }
#
# result = es.search(index='news', body=dsl)
# print(json.dumps(result, indent=2, ensure_ascii=False))
# body = {'title': '好想你'}
# result = es.indices.create(index='good',ignore=400)
# print(result)
# result = es.index(index='good', id=body['title'], body={'title': '好想你'})
# print(result)
# result = es.index(index='good',id=body['title'], body={'title': '好想你'})
# print(result)
# result = es.index(index='good',id=body['title'], body={'title': '新世界'})
# print(result)

a = [1,2,3,4]
print(" ".join(str(i) for i in a))


