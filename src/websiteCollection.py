from Website import Website

class QS(Website):
    '''
    Top Univeristies scrapper inherted from the Website Abstract class.

    :Override Fucntions:
     - getAllRows - get by click the show all button on the page.
     - parse
    '''
    def __init__(self):
        super().__init__("QS",
            "https://www.topuniversities.com/university-rankings/world-university-rankings/{}" )

    def getAllRows(self):
        page_src = self.expandByClickAll(
            select_xpath = '//*[@id="qs-rankings_length"]/label/span[2]/span[2]', 
            all_xpath = '//*[@id="qs-rankings_length"]/label/span[2]/div/div/span/span/ul/li[5]/span')

        for uni in page_src.find('tbody').find_all('tr'):
            yield uni

    def parse(self, row):
        rank = self.rankFormat(row.find(attrs = {'class' : 'rank'}).text)
        name = row.find(attrs = {'class' : 'title'}).text
        logo = row.find('img')['src'] if row.find('img') else None
        country = row.find(attrs = {'class' : 'country'}).text
        
        return {
            'Name' : name,
            'Logo' : logo,
            'Country' : country,
            'Subject' : 'All',
            'Organisation' : self.name,
            'Year' : self.year,
            'Rank' : rank
        }

class Times(Website):
    '''
    Times Higer Education scrapper inherted from the Website Abstract class.

    :Override Fucntions:
     - getAllRows - get by click the show all button on the page.
     - parse
    '''
    def __init__(self):
        super().__init__("Times", 
            "https://www.timeshighereducation.com/world-university-rankings/{}/world-ranking#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/stats")

    def getAllRows(self):
        page_src = self.expandByClickAll(all_xpath = '//*[@id="datatable-1_length"]/label/select/option[5]')
        
        for uni in page_src.find('tbody').find_all('tr'):
            yield uni
    
    def parse(self, row):
        rank = self.rankFormat(row.find(attrs = {'class' : 'rank sorting_1 sorting_2'}).text)
        name = row.find(attrs = {'class' : 'ranking-institution-title'}).text
        country = row.find(attrs = {'class' : 'location'}).text

        return {
            'Name' : name,
            'Logo' : None,
            'Country' : country,
            'Subject' : 'All',
            'Organisation' : self.name,
            'Year' : self.year,
            'Rank' : rank
        }
        
class ARWU(Website):
    '''
    Shanghairanking Academic Ranking of World Universities scrapper inherted from the Website Abstract class.

    :Override Fucntions:
     - getAllRows - get by click the show all button on the page.
     - parse
    '''
    def __init__(self):
        super().__init__("ARWU", "http://www.shanghairanking.com/ARWU{}.html")
    
    def getAllRows(self):
        page_src = self.soup(self.driver.page_source)
        
        first = True
        for uni in page_src.find('tbody').find_all('tr'):
            if first:
                first = False
                continue
            yield uni
    
    def parse(self, row):
        rank = self.rankFormat(row.find('td').text)
        uni = row.find_all(attrs = {'target' : '_blank'})
        name = uni[0].text
        country = uni[1]['title'].replace("View universities in ", "").replace(".", "")
        
        return {
            'Name' : name,
            'Logo' : None,
            'Country' : country,
            'Subject' : 'All',
            'Organisation' : self.name,
            'Year' : self.year,
            'Rank' : rank
        }