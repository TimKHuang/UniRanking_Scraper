from websiteCollection import QS, Times
from SQLiteDB import SQLiteDB

def run():
    db = SQLiteDB('ucollege.db')
    db.insertAll(Times().scrapeAll(2011, 2020))
    db.insertAll(QS().scrapeAll(2012, 2020))

if __name__ == "__main__":
    run()