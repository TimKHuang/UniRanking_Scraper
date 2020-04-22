from Website import Webiste
from bs4 import BeautifulSoup

class QS(Webiste):

    def __init__(self):
        super().__init__("QS",
            "https://www.topuniversities.com/university-rankings/world-university-rankings/{}" )

    def getAllRows(self):
        page_src = self.expandByClickAll(
            select_xpath = '//*[@id="qs-rankings_length"]/label/span[2]/span[2]', 
            all_xpath = '//*[@id="qs-rankings_length"]/label/span[2]/div/div/span/span/ul/li[5]/span')

        soup = BeautifulSoup(page_src, 'html5lib')
        universityCollection = soup.find('tbody').find_all('tr')
        for uni in universityCollection:
            yield uni

    def parse(self, row):
        rank = self.rankFormat(row.find(attrs = {'class' : 'rank'}).text)
        name = row.find(attrs = {'class' : 'title'}).text
        logo = row.find('img')['src'] if row.find('img') else None
        country = row.find(attrs = {'class' : 'country'}).text
        return {
            'name' : name,
            'logo' : logo,
            'country' : country,
            'subject' : 'All',
            'org' : self.name,
            'year' : self.year,
            'rank' : rank
        }

