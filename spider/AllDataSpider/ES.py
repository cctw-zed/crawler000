import json
from elasticsearch import Elasticsearch

class ES(object):

    def __init__(self, indexName):
        # 默认host为localhost，port为9200，也可以手动指定
        self.es = Elasticsearch()
        self.indexName = indexName
        self.mapping = {
            'properties': {
                'title': {
                    'type': 'text',
                    'analyzer': 'ik_max_word',
                    'search_analyzer': 'ik_max_word'
                },
                'abstract': {
                    'type': 'text',
                    'analyzer': 'ik_max_word',
                    'search_analyzer': 'ik_max_word'
                }
            }
        }

    def Delete(self):
        self.es.indices.delete(index=self.indexName , ignore=[400,404,409])

    def InsertData(self, body):
        # 将主键id修改为title，防止重复。且index函数自带更新功能
        result = self.es.index(index=self.indexName ,id=body['title'],ignore=[400,409],body=body)
        print(result)

    def isExist(self, title):
        return self.es.exists(index=self.indexName, id=title)
        # if result:
        #     print('该页面已存在')
        # return  result

    def search(self, *args):
        keyword = " ".join(str(i) for i in args)
        dsl = {
            'size': 1000,
            'query': {
                'bool': {
                    'should': {'match':{'title': keyword}},
                    'must': {'match':{'abstract': keyword}}
                },
            },
        }
        result = self.es.search(index=self.indexName, body=dsl, ignore=404)
        return result
        # print(result['hits']['hits'][0]['_source'])
        # print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
     es = ES('allspider')
     result = es.search(['会议'])
     print(len(result["hits"]["hits"]))
     #for item in result["hits"]["hits"]:
     #    print(item["_source"])
#    es = Elasticsearch()
#    es.indices.create(index='allspider', ignore=[400,404])
#    mapping = {
#        'properties': {
#            'title': {
#                'type': 'text',
#                'analyzer': 'ik_max_word',
#                'search_analyzer': 'ik_max_word'
#            },
#            'abstract': {
#                'type': 'text',
#                'analyzer': 'ik_max_word',
#                'search_analyzer': 'ik_max_word'
#            }
#        }
#    }
#    result = es.indices.put_mapping(index='allspider', body=mapping)
#    print(result)
    # result['hits']['hits']
