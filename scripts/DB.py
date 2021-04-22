from pymongo import MongoClient
from tinydb import TinyDB


def insert(table,data):
    db=TinyDB(table)
    db.insert(data)

def get_all(table):
    db = TinyDB(table)
    return db.all()

class MongoDB():
    def __init__(self,db=None):
        connection=MongoClient("mongodb://localhost:27017")
        if db==None:
            self.db=connection["StockData"]
        else:
            self.db=connection[db]
        self.collection=self.db["company"]

    def insert(self,data):
        self.collection.insert(data)

    def getAll(self):
        return [i for i in self.collection.find()]

    def update(self,pid,value):
        myquery = {"ticker": pid}
        newvalues = {"$set": {"previousClose": value}}

        self.collection.update_one(myquery, newvalues)
'''
mongo=MongoDB()
mongo.insert({"com":"ABC","price":100})
print(mongo.getAll())
'''