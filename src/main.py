from websiteCollection import QS
from SQLiteDB import SQLiteDB

def run():
    db = SQLiteDB('ucollege_oop_test.db')
    db.insertAll(QS().scrape(2020))

if __name__ == "__main__":
    run()