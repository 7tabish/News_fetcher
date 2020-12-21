import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


def get_news(API_KEY,KEYWORDS):
    KEYWORDS=str(KEYWORDS)
    KEYWORDS=KEYWORDS.lower()
    url = ('http://newsapi.org/v2/everything?'
           'q={}&'
           'apiKey={}').format(KEYWORDS,API_KEY)
    response = requests.get(url)
    data=json.loads(response.text)
    urls=[]
    for content in data['articles']:
        print('title  {}: '.format(content['title']))
        print('url {}'.format(content['url']))
        urls.append(content['url'])


    driver =None
    for url in urls:
        try:
            data=''
            print('reading  {}'.format(url))
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(url)
            driver.implicitly_wait(15)
            print('Please wait 4 seconds..')
            time.sleep(4)
            bs1 = BeautifulSoup(driver.page_source, features='html.parser')
            paragraphs = bs1.find_all('p')
            if len(paragraphs) < 0:
                print('no content found !')
            for text in paragraphs:
                data=data+text.getText()
            #convert all the text to lower to match with our keyword ( no conflicts with capital letters)
            data = data.lower()
            occurence_frequency = data.count(KEYWORDS)
            # get the string after split of first target keyword but it removes the keyword from the start of string we will add it later
            split_string = data.split(KEYWORDS, 1)[1]
            # get the last occurance of your target keyword, remove the keyword from the last of the string, we will add it later
            last_occ = split_string.rfind(KEYWORDS)

            #adding keyword at the start and end of the string
            filtered_data = KEYWORDS+' ' + split_string[:last_occ] + ' '+KEYWORDS
            print(filtered_data)
            print('----------------------------')

        except Exception as e:
            print('Error ', e)

        finally:
            driver.close()



get_news('API KEY','tesco')