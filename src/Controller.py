from SQLiteDB import SQLiteDB
from InfoChecker import InfoChecker
from websiteCollection import QS, Times, ARWU, CWTS

class Controller:
    '''
    The controller of the whole program.

    :Attributes:
     - Dict avaiableYear - The range of available years of differnet organisations.
     - List availableWebsite - the webiste object 
     - String name - connected database address
     - InfoChecker monitor - check the infomation
    
    :Functions:
     -
    '''

    availableYear = {
        'QS' : [2012, 2020],
        'Times' : [2011, 2020],
        'ARWU' : [2003, 2019],
        'CWTS' : [2013, 2019],
    }

    availableWebsite = [QS(), Times(), ARWU(), CWTS()]

    def __init__(self, name):
        self.db =  SQLiteDB(name)
        self.monitor = InfoChecker()
    
    def check(self, universityDetail):
        '''
        Do the full check of the university

        :Args:
         - Dict universityDetail - The detail of the university
        
        :Returns:
         - Dict result - the checked detail
        '''
        checkedname = self.monitor.check(universityDetail['Name'])
        return {
            'Name': checkedname,
            'Logo': self.monitor.getLogo(checkedname, logo=universityDetail['Logo']),
            'Country': self.monitor.check(universityDetail['Country'], country=True),
            'Subject': universityDetail['Subject'],
            'Organisation': universityDetail['Organisation'],
            'Year': universityDetail['Year'],
            'Rank': universityDetail['Rank'],
        }

    def checkAll(self, listOfUnis):
        '''
        Helper Function to check 

        :Args:
         - List listOfUnis - List of the detail of the university
        
        :Returns:
         - List result - List of the checked detail
        '''
        return [ self.check(university) for university in listOfUnis]

    def run(self):
        websiteData = []
        for website in self.availableWebsite:
            websiteData += website.scrapeAll(
                self.availableYear[website.name][0],
                self.availableYear[website.name][1]
            )
        
        self.db.insertAll(self.checkAll(websiteData))
    
    def test(self):
        print(self.checkAll(QS().scrape(2012)))
    

