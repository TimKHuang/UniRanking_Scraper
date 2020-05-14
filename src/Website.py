from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
from bs4 import BeautifulSoup

class Website(ABC):
    """
    Abstract Class of a certain ranking website. Provide basic scrape function.

    :Attributes:
     - string url_format - a string with {} holding the place for the year to scrape.
     - string name - name of the website / organisation
     - int year - the year to scrape. Initialised in the scrape(year)
     - webdriver driver - the driver of the browser. Initialised in the scrape(year)

    :Funcitons:
    - scrape - scrape the website given a certain year.

    :ABmethod:
     - getAllRows - find and return all the rows in the rank table
     - parse - parse the source of a row into a dictionary

    :Helper:
     - expandByClickAll - Function that expands to show the whole content of the page
     - getNextPage - Function that yields a page each time
     - rankFormat - Function that translate the rank from string to int
    """

    def __init__(self, name, url_format):
        """
        Constructor of the class

        :Args:
         - string url_format - a string with {} holding the place for the year to scrape.
         - string name - name of the website / organisation
        """
        self.url_format = url_format
        self.name = name

    def scrape(self, year):
        """
        Scrape the website given the year and return the data.

        :Args:
         - int year - the year to scrape
        
        :Returns:
         - List<Dictionary> - The data scraped. The content of the dictiontary is defined in 
            the docstring of parse(self, row)
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

    def scrapeAll(self, start, end):
        '''
        Scrap a range of year. Inclusive on both end.
        print the years that has raised an error.

        :Args:
         - int start - the start year
         - int end - the end year
        
        :Returns:
        - List<Dictionary> - The data scraped. The content of the dictiontary is defined in 
            the docstring of parse(self, row)
        '''
        result = []
        for year in range(start, end+1):
            try:
                result += self.scrape(year)
            except Exception as e:
                print(year)
                print(e)
        return result
        
    @abstractmethod
    def getAllRows(self):
        """
        By analysing the page source to get all the rows in the rank table.

        :Yield:
         - soup row - a row that is get by the soup analysing the page source.
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
             'Name' : string
             'Logo' : string - url to the logo picture. None if not.
             'Country' : string
             'Subject' : string
             'Organisation' : string - the organisation runs the ranking. Should be self.name normally.
             'year' : int - the year this ranking result is published. Should be self.year normally.
             'rank' : int - the year should be an integer instead of string like '600+' and '800-100'.
                A helper formatting function can be called by super.rankFormat(rank).
            }
        """
        pass

    def soup(self, page_src):
        '''
        Get the souped page source

        :Args:
         - html page_src - the source of the page

        :Returns:
         - soup - the souped page using html5lib
        '''
        return BeautifulSoup(page_src, 'html5lib')

    def expandByClickAll(self, *, select_xpath = None, all_xpath):
        """
        Expand the page to show all and yield all the table rows.

        :Args:
         - string select_xpath - the relative xpath to the button that select the number to display in a page.
            If None, means the programme can directly click the All button.
         - string all_xpath - the relative xpath to the button of showing all

        :Returns:
         - soup src - the source of the expanded page that has been analysed use beautifulSoup with html5lib.
        """
        while(True):
            try:
                self.driver.execute_script('window.scrollBy(0,500)')
                if(select_xpath):
                    self.driver.find_element_by_xpath(select_xpath).click()
                self.driver.find_element_by_xpath(all_xpath).click()
                break
            except (NoSuchElementException, ElementClickInterceptedException):
                continue
        
        sleep(5)
        return self.soup(self.driver.page_source)

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
        result = ""
        isNumber = False
        for char in rank:
            if char.isdigit():
                isNumber = True
                result += char
                continue
            if isNumber:
                break
        return int(result)