from tinydb import TinyDB


def insert(table,data):
    db=TinyDB(table)
    db.insert(data)

def get_all(table):
    db = TinyDB(table)
    return db.all()