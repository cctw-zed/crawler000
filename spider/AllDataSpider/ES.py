import json
from elasticsearch import Elasticsearch

class ES(object):

    def __init__(self):
        # 默认host为localhost，port为9200，也可以手动指定
        self.es = Elasticsearch()
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
        self.es.indices.delete(index='spider', ignore=[400,404,409])

    def InsertData(self, body):
        # 将主键id修改为title，防止重复。且index函数自带更新功能
        result = self.es.index(index='spider',id=body['title'],ignore=[400,409],body=body)
        print(result)

    def search(self, *args):
        keyword = " ".join(str(i) for i in args)
        dsl = {
            'size':100,
            'query': {
                'bool': {
                    'should': {'match':{'title': keyword}},
                    'must': {'match':{'abstract': keyword}}
                },
            },
        }
        result = self.es.search(index='spider',body=dsl,ignore=404)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    # es = ES()
    # es.search(['人民','代表大会'])
    es = Elasticsearch()
    es.indices.create(index='spider', ignore=[400,404])
    mapping = {
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
    result = es.indices.put_mapping(index='spider', body=mapping)
    print(result)
