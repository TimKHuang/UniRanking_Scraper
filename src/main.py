from websiteCollection import QS, Times, ARWU, CWTS
from SQLiteDB import SQLiteDB

def run():
    db = SQLiteDB('result/ucollege.db')
    # db.insertAll(Times().scrapeAll(2011, 2020))
    # db.insertAll(QS().scrapeAll(2012, 2020))
    # db.insertAll(ARWU().scrapeAll(2003, 2019))
    db.insertAll(CWTS().scrapeAll(2013, 2019))

def test():
    print(CWTS().scrape(2013))

if __name__ == "__main__":
    run()