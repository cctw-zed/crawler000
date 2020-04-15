from pymongo import MongoClient
from MyBloom import MyBloom


class MyMongoDB(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.crawlSpider
        self.dbCollection = self.db.baidu_infos
        self.col_working = self.db.workings
        self.mybloom = MyBloom()
    # 插入一条结果
    def insert(self, res):
        if res['real_url'] != "" and res['title'] != "" and res['abstract'] !="":
            if self.mybloom.isExist(res['title']):
                self.dbCollection.insert_one(res)
    # 在working表中删除关键词
    def deleteKeyword(self, keyword):
        self.col_working.delete_one({"keyword": keyword})
