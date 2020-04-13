from pymongo import MongoClient


class MyMongoDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.crawlSpider
        self.dbCollection = self.db.baidu_infos
        self.col_working = self.db.workings
    # 插入一条结果
    def insert(self, res):
        self.dbCollection.insert_one(res)
    # 在working表中删除关键词
    def deleteKeyword(self, keyword):
        self.col_working.delete_one({"keyword": keyword})
