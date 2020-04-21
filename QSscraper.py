from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import sqlite3


# These are the constants

def get_src(year):
    print(str(year)+ " HAS STARTED")

    url = "https://www.topuniversities.com/university-rankings/world-university-rankings/" + str(year)

    # open the website
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(15)


    # expand all the widget by clicking the all
    while(True):
        try:
            driver.execute_script('window.scrollBy(0, 500)')
            driver.find_element_by_xpath('//*[@id="qs-rankings_length"]/label/span[2]/span[2]').click()
            driver.find_element_by_xpath('//*[@id="qs-rankings_length"]/label/span[2]/div/div/span/span/ul/li[5]/span').click()
            break
        except:
            continue
        
    sleep(5)

    # get the html sorce codes
    pageSrc = driver.page_source
    driver.close()

    print("Suceessfully get the scource code")

    return pageSrc

def parser(html, year):
    
    soup = BeautifulSoup(html, 'html5lib')

    #find the main body of the ranking
    universityCollection = soup.find('tbody').find_all('tr')

    result = []

    for uni in universityCollection:
        rank = uni.find(attrs = {'class' : 'rank'}).text
        rank = rank.replace("=", '')
        rank = rank.replace("+", '')
        rank = rank.split('-')[0]
        name = uni.find(attrs = {'class' : 'title'}).text
        logo = uni.find('img')
        logo = None if logo == None else logo['src'] 
        country = uni.find(attrs = {'class' : 'country'}).text
        result.append({
            'rank': int(rank), 
            'name': name, 
            'logo': logo, 
            'subject': "All",
            'org': "QS",
            'year': year,
            'country':country
            })

    print('Successfully Parse the source code')

    return result

def txtOutputer(result):
    output = open('QSrank.txt', 'w')

    for dictionary in result:
        output.write(dictionary['rank']  + '\t' + dictionary['name'] + '\t' + dictionary['country'] + '\n')
    
    output.close()

    print('File writing finished.')

def database_initialise():
    uni_db = sqlite3.connect('ucollege.db')
    uni_c = uni_db.cursor()
    try:
        uni_c.execute('''CREATE TABLE Rank
            (Name TEXT NOT NULL, 
            Logo TEXT,
            Country TEXT NOT NULL, 
            Subject TEXT NOT NULL, 
            Org TEXT NOT NULL, 
            Year INT NOT NULL,
            Rank INT NOT NULL);''')
    except:
        pass
    uni_db.commit()
    uni_db.close()

def databaseOutput(result):
    database_initialise()

    uni_db = sqlite3.connect('ucollege.db')
    uni_c = uni_db.cursor()

    for dictionary in result:
        if dictionary['logo'] == None:
            if "'" in dictionary["name"]:
                uni_c.execute('INSERT INTO Rank VALUES ("{}", NULL, "{}", "{}", "{}", {}, {});'.format(
                    dictionary['name'],
                    dictionary['country'],
                    dictionary['subject'],
                    dictionary['org'],
                    dictionary['rank'],
                    dictionary['year']))
            else:
                uni_c.execute("INSERT INTO Rank VALUES ('{}', NULL, '{}', '{}','{}', {}, {});".format(
                    dictionary['name'],
                    dictionary['country'],
                    dictionary['subject'],
                    dictionary['org'],
                    dictionary['rank'],
                    dictionary['year']))
            continue

        if "'" in dictionary["name"]:
            uni_c.execute('INSERT INTO Rank VALUES ("{}", "{}", "{}", "{}", "{}", {}, {});'.format(
                dictionary['name'],
                dictionary['logo'],
                dictionary['country'],
                dictionary['subject'],
                dictionary['org'],
                dictionary['rank'],
                dictionary['year']))
        else:
            uni_c.execute("INSERT INTO Rank VALUES ('{}', '{}', '{}', '{}','{}', {}, {});".format(
                dictionary['name'],
                dictionary['logo'],
                dictionary['country'],
                dictionary['subject'],
                dictionary['org'],
                dictionary['rank'],
                dictionary['year']))

    uni_db.commit()
    uni_db.close()
    print("SUCCESSFULLY SAVED")


def main():
    for i in range(9):
        databaseOutput(parser(get_src(2012+i), 2012 + i))

if __name__ == '__main__':
    main()
