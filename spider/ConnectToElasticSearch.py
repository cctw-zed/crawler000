from MyBloom import MyBloom
from elasticsearch import Elasticsearch


class ConnectToElasticSearch(object):

    def __init__(self):
        self.es = Elasticsearch()
        self.indexName = 'prespider'
        self.mybloom = MyBloom()

    # 创建新的Index，并添加mapping
    def newIndex(self):
        # 为新的index添加mapping，用于中文分词
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
        if not self.es.indices.exists(index=self.indexName):
            self.es.indices.create(index=self.indexName, ignore=400)
            result = self.es.indices.put_mapping(body=mapping,index=self.indexName)
            print(result)
        else:
            print('该index已存在，创建失败！')

    # 插入数据
    def insert(self, res):
        if res['real_url'] is not None and res['title'] is not None and res['abstract'] is not None:
            if self.mybloom.isExist(res['title']):
                result = self.es.index(index=self.indexName, id=res['title'], body=res, ignore=[400,409])
                print(result)
        print('未插入')

    # 在working表中删除关键词
    # def deleteKeyword(self, keyword):
    #     self.col_working.delete_one({"keyword": keyword})
    #     result = self.es.indices.delete(index=self.col_working, id=keyword, ignore=[400,404])
    #     print('删除working表： ' + result)

if __name__ == '__main__':
    ConnectToES = ConnectToElasticSearch()
    ConnectToES.newIndex()