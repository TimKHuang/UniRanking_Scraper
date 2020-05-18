import sqlite3

class SQLiteDB:
    '''
    A SQLite3 Database manager designed specific for UniRanking Sracpper data processing.

    :Attributes:
     - string db_name - the name of the databse. example: 'ranking.db'
     - database - the database returned from the sqlite3.connect()
     - cursor - the cursor of the database
    
    :Functions:
     - __init__ - constructer. It calls connect() and creatTable()
     - connect - connect to a database
     - createTable - create a table in the database
     - save - commit the change to the database
     - close - close the database. connect() need to be called again to use other functions.
     - insert - insert a university info into the table
     - insertAll - insert a list of univeristy info into the table.
     - contains - Check if the Translate contains the name
     - insertTranslate - insert the translated name into the table
     - fetchall - Fetch all the data from a table
    '''
    def __init__(self, db_name):
        '''
        Constructor. Set up the fist connect and create  the fist table called Rank.

        :Args:
         - string db_name - the name of the database. Must end in .db
        '''
        self.database = None
        self.cursor = None
        self.db_name = db_name
        self.connect()
        self.createTable()
    
    def connect(self, db_name = None):
        '''
        Connect to a local database.
        Attempting to connect a new database without call close() first will automatically close the database.

        :Args:
         - string db_name - the name of the database. Must end in .db
        '''
        if(db_name):
            self.db_name = db_name
        if(self.database):
            self.close()
        self.database = sqlite3.connect(self.db_name)
        self.cursor = self.database.cursor()
    
    def save(self):
        '''
        Save the changes has been made to the database. Same as commit.
        '''
        self.database.commit()
    
    def close(self):
        '''
        Close the current database.
        Attempting to do other things will cause error.
        '''
        self.database.close()
        self.cursor = None
        self.database = None

    def createTable(self, table_name = 'Rank'):
        '''
        Create a table. The content is not changable.
        Attempting to create an existing table will be ignored.

        :Args:
         - string table_name - the name of the created table. Default: Rank
        '''
        try:
            self.cursor.execute('''CREATE TABLE {}
                    (Name TEXT NOT NULL, 
                    Logo TEXT,
                    Country TEXT NOT NULL, 
                    Subject TEXT NOT NULL, 
                    Organisation TEXT NOT NULL, 
                    Year INT NOT NULL,
                    Rank INT NOT NULL);'''.format(table_name))
        except:
            pass

        try:
            self.cursor.execute('''CREATE TABLE 'Translate'
                    (en TEXT NOT NULL, 
                    cn TEXT NOT NULL);''')
        except:
            pass
    
    def insert(self, uni_dictionary, table_name = 'Rank'):
        '''
        Insert the uni Info to the dictionary.
        Suggest use the provided abstarct class Webiste to get the dicitionary formatting.
        Save automatically.

        :Args:
         - dicitionary uni_dictionary - the dictionary contains uni information.
         - string table - the table to insert. Default: Rank
        '''
        if(len(uni_dictionary['Name']) == 0 or len(uni_dictionary['Country']) == 0):
            return 
            
        if uni_dictionary['Logo'] == None:
            if "'" in uni_dictionary["Name"]:
                script = 'INSERT INTO {} VALUES ("{}", NULL, "{}", "{}", "{}", {}, {});'
            else:
                script = "INSERT INTO {} VALUES ('{}', NULL, '{}', '{}','{}', {}, {});"
            script = script.format(table_name,
                    uni_dictionary['Name'],
                    uni_dictionary['Country'],
                    uni_dictionary['Subject'],
                    uni_dictionary['Organisation'],
                    uni_dictionary['Year'],
                    uni_dictionary['Rank'])
        else:
            if "'" in uni_dictionary["Name"]:
                script = 'INSERT INTO {} VALUES ("{}", "{}", "{}", "{}", "{}", {}, {});'
            else:
                script = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}','{}', {}, {});"
            script = script.format(table_name,
                    uni_dictionary['Name'],
                    uni_dictionary['Logo'],
                    uni_dictionary['Country'],
                    uni_dictionary['Subject'],
                    uni_dictionary['Organisation'],
                    uni_dictionary['Year'],
                    uni_dictionary['Rank'])
        self.cursor.execute(script)
        self.save()
    
    def insertAll(self, list, table_name = 'Rank'):
        '''
        Insert all the dictionary from a list.
        Suggest use the provided abstarct class Webiste to get the dicitionary formatting.
        Save automatically.

        :Args:
         - list list - the list of all the info dictionaries
         - string table - the table to insert. Default: Rank
        '''
        for uni_dictionary in list:
            self.insert(uni_dictionary, table_name)

    def contains(self,name):
        '''
        Check if the Translate contains the name

        :Args:
         - String name - the english name
        
        :Returns:
         - bool result - is it contained or not
        '''
        rows = self.fetchall('Translate')
        for row in rows:
            print(row[0])
            if row[0] == name:
                return True
        
        return False
    
    def insertTranslate(self, en, cn):
        '''
        insert the translated name into the table

        :Args:
         - String en - the english name
         - String cn - Translated Chinese name
        '''
        self.cursor.execute('INSERT INTO Translate VALUES ("{}", "{}");'.format(en, cn))
        self.save()

    def fetchall(self, table):
        '''
        Fetch all the data from a table

        :Args:
         - String table - Table name
        
        :Returns:
         - Tuple result - result tuple
        '''
        self.cursor.execute('SELECT * FROM {}'.format(table))
        return self.cursor.fetchall()