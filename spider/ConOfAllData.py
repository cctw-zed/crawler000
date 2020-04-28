from pymongo import MongoClient
from pybloom_live import ScalableBloomFilter


class ConOfAllData:
    def __init__(self, site_name):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.crawlSpider
        self.col_url = self.db[site_name+"_url"]
        self.col_content = self.db[site_name+"_content"]
        self.sbf = ScalableBloomFilter(initial_capacity=100)
        for item in self.col_url.find():
            self.sbf.add(item["url"])
        self.insert_url = []
        self.insert_content = []

    def isexist(self, url):
        if url in self.sbf:
            return True
        else:
            self.sbf.add(url)
            self.insert_url.append({"url": url})
            return False

    def insert(self, content):
        if content['real_url'] is not None and content['title'] is not None and content['abstract'] is not None:
            self.insert_content.append(content)

    def end(self):
        if len(self.insert_url) != 0:
            self.col_url.insert_many(self.insert_url)
        if len(self.insert_content) != 0:
            self.col_content.insert_many(self.insert_content)


#if __name__ == "__main__":
    #coad = ConOfAllData("ningxia")
    #coad.isexist("1")
    #coad.isexist('2')
    #coad.isexist("1")
    #coad.insert({"site": "ningxia"})
    #coad.insert({"site": "guangdong"})
    #coad.end()