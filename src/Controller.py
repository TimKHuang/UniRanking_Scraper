from SQLiteDB import SQLiteDB
from InfoChecker import InfoChecker
from Translator import Translator
from websiteCollection import QS, Times, ARWU

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
    }

    availableWebsite = [QS(), Times(), ARWU()]

    def __init__(self, name):
        self.db =  SQLiteDB(name)
        self.monitor = InfoChecker()
        self.translator = Translator()
    
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

    def translate(self, word):
        '''
        Translate a word and insert into the database

        :Args:
         - String word - the word to be translated
        '''
        print(word)
        if self.db.contains(word):
            return
        
        translated = self.translator.toChinese(word)
        print(translated)
        self.db.insertTranslate(word, translated)

    def translateAll(self):
        '''
        Translate all the word in the table
        '''
        rows = self.db.fetchall('Rank')
        for row in rows:
            self.translate(row[0])
            self.translate(row[2])
            self.translate(row[3])

    def run(self):
        websiteData = []
        for website in self.availableWebsite:
            websiteData += website.scrapeAll(
                self.availableYear[website.name][0],
                self.availableYear[website.name][1]
            )
        
        self.db.insertAll(self.checkAll(websiteData))
    
    def test(self):
        self.translateAll()

