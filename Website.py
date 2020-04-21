from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup

class Webiste(ABC):

    def __init__(self, name, url_format):
        self.url_format = url_format
        self.name = name

    def scrape(self, year):
        """
        Scrape the website given the year and return the data.

        :Args:
         - int year - the year to scrape
        
        :Returns:
         - List<Dictionary> - The data scraped. The content of the dictiontary is defined in 
            the dostring of parse(self, row)
        """
        self.year = year
        
        url = self.url_format.format(year)
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        sleep(15)
        
        result = []
        for row in self.getAllRows():
            result.append(self.parse(row))
        
        self.driver.close()
        return result
        
    @abstractmethod
    def getAllRows(self):
        """
        By analysing the page source to get all the rows in the rank table.

        :Yield:
         - soup row - a row that is get by the soup analysing the page source.
        
        :Helper:
         - expandByClickAll - Function that expands to show the whole content of the page
         - getNextPage - Functino that yields a page each time
        """
        pass
    
    
    @abstractmethod
    def parse(self, row):
        """
        Parse the source code of a row and return a dictionary of the results

        :Args:
         - soup row - a row that is get by the soup analysing the page source.

        :Returns:
         - dictionary university {
             'name' : string
             'logo' : string - url to the logo picture. None if not.
             'country' : string
             'subject' : string
             'org' : string - the organisation runs the ranking. Should be self.name normally.
             'year' : int - the year this ranking result is published. Should be self.year normally.
             'rank' : int - the year should be an integer instead of string like '600+' and '800-100'.
                A helper formatting function can be called by super.rankFormat(rank).
            }
        """
        pass

    # getResult() will reutrn the closed finished result  
    def getResult(self):
        # TODO
        pass

    # This two helper functions below offers easy ways to override the __getAllRow
    def expandByClickAll(self, *, select_xpath = None, all_xpath):
        """
        Expand the page to show all and yield all the table rows.

        :Args:
         - string select_xpath - the relative xpath to the button that select the number to display in a page.
            If None, means the programme can directly click the All button.
         - string all_xpath - the relative xpath to the button of showing all

        :Returns:
         - src - the source of the expanded page.
        """
        while(True):
            try:
                self.driver.execute_script('window.scrollBy(0,500)')
                if(select_xpath):
                    self.driver.find_element_by_xpath(select_xpath).click()
                self.driver.find_element_by_xpath(all_xpath).click()
            except NoSuchElementException:
                continue
        
        sleep(5)
        return self.driver.page_source

    def getNextPage(self, *, next_xpath):
        # TODO
        pass

    def rankFormat(self, rank):
        """
        Remove chars in the string and return int.

        :Args:
         - string rank - origin text of rank
        
        :Returns:
         - int rank - a single rank integer
        """
        return int(rank.replace("=", '').replace("+", '').split('-')[0].strip())