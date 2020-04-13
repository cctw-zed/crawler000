from pymongo import MongoClient


class MyMongoDB:
    def __init__(self, url, port, db_name, col_name):
        self.client = MongoClient(url, port)
        self.db = self.client[db_name]
        self.col = self.db[col_name]

    def Insert_Many_Items(self, mylist):
        self.col.insert_many(mylist)
