import wikipedia

class InfoChecker:
    '''
    A Class to check all the infomation.

    :Attributes:
     - Dict logoCollection - to store the provided logo
    
    :Functions:
     - check - Check the name infomation
     - getLogo - the the logo url
    '''

    def __init__(self):
        self.logoCollection = {}

    def check(self, orginal_name, country = False):
        '''
        Given a name, use wikipedia to get the official full name

        :Args:
         - String name - the orginal name

        :Returns:
         - Stirng name - the checked name
        '''
        name = orginal_name.lower()

        if(country):
            if ( 'tw' in name and 'china' in name ) or 'taiwan' in name:
                return 'Taiwan, China'
            
            if ( 'hk' in name and 'china' in name) or 'hong kong' in name:
                return 'Hong Kong, China'
            
            if 'macau' in name or 'macao' in name:
                return 'Macao, China'

            if 'china' in name:
                return 'Mainland, China'

        if 'univ' in name and 'unive' not in name:
                name.replace ('univ', 'university')

        try:
            return wikipedia.search(name)[0]
        except:
            print(orginal_name + " NOT CHECKED")
            return orginal_name

    def getLogo(self, name, logo = None):
        '''
        Given a name, return the logo. 
        Store the logo if it has not been stored.

        :Args:
         - String name - the name of the university
         - String logo - optionally provide the logo url
        
        :Returns:
         - String logo - None if no stored logo and not provide a logo.
        '''
        if name in self.logoCollection.keys():
            return self.logoCollection[name]

        if logo:
            self.logoCollection[name] = logo
            
        return logo