
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import itertools
import csv

geckodriver_path = 'E:/geckodriver.exe'

service = Service(executable_path=geckodriver_path)

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
#driver = webdriver.Firefox(service=service)

import time

def execute_selenium_script(topic):
    driver.get('https://twitter.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJsYW5nIjoiZW4ifQ%3D%3D%22%7D')
    try:
        driver.implicitly_wait(10)
        element=WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')))
        element.send_keys('fahadholalkere123@gmail.com')
    except WebDriverException:
        print("Tweets did not appear!, Try setting headless=False to see what is happening")
        
    driver.find_element('xpath','/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]').click()
    driver.implicitly_wait(10)
    try:
        elementp=WebDriverWait(driver,10).until(EC.presence_of_element_located(('xpath', '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')))
        elementp.send_keys('Fahadholalkere')
    except WebDriverException:
        print("Username not required")
    driver.find_element('xpath','/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div').click()
    driver.implicitly_wait(10)
    try:
        elementp=WebDriverWait(driver,10).until(EC.presence_of_element_located(('xpath', '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
        elementp.send_keys('Siraj$$$')
    except WebDriverException:
        print("Tweets did not appear!, Try setting headless=False to see what is happening")
    driver.find_element('xpath','/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div').click()
    driver.implicitly_wait(10)


    element=driver.find_element('xpath','/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input')
    element.send_keys(topic)
    element.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)

    # posts=["https://twitter.com/MuhammadSmiry/status/1711432890918002698","https://twitter.com/AyaIsleemEn/status/1711015598694473875","https://twitter.com/OnlinePalEng/status/1711450403227742258","https://twitter.com/HananyaNaftali/status/1710699051484692589","https://twitter.com/NourNaim88/status/1729908949544268265","https://twitter.com/itranslate123/status/1728778270764617831","https://twitter.com/swilkinsonbc/status/1728442539273818460"]

    # tfile=['t1.csv','t2.csv','t3.csv','t4.csv','t5.csv','t6.csv','t7.csv']
    # len1=len(posts)
    # for str in range(len1):
    #driver.get(posts[str])
    driver.implicitly_wait(10)



    time.sleep(5)
        
    tweets = []
    result = False
    old_height = driver.execute_script("return document.body.scrollHeight")
    count=0
    driver.execute_script("window.scrollTo(0,15)")

    time.sleep(2)

    all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

    while result==False:

        for item in all_tweets[1:]: 
            try:
            
                ad_indicator = item.find_elements(By.XPATH, './/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0" and contains(text(), "Ad")]')
                if ad_indicator:
                    print("Skipping ad tweet")
                    continue 
            except StaleElementReferenceException:
                print("Stale element exception, refreshing elements.")
                all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
                continue

            print('--- text ---')
            try:
                text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
            except:
                text = 'empty'
            print(text)
            
            print('--- Date ---')
            try:
                date = item.find_element(By.XPATH, './/div[@data-testid="User-Name"]/div[2]/div/div[3]/a/time').text
            except:
                date = 'empty'
            print(date)

            if text!='empty' and text!='':
                tweets.append([ text, date])
        
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        time.sleep(2)
    
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == old_height:
            result = True
        old_height = new_height

        all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
        
        time.sleep(2)
        
        all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

        count=count+1




        csv_file_name = 'tweet_file.csv'

        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(tweets)

        print(f'CSV file "{csv_file_name}" has been created.')

    # posts = ["https://twitter.com/jacksonhinklle/status/1735488614854009217",
    #          "https://twitter.com/kiyahwillis/status/1736549287386083799",
    #          "https://twitter.com/Naila_Ayad/status/1736625338027745532",
    #          "https://twitter.com/abierkhatib/status/1735321866179391974",
    #          "https://twitter.com/mhdksafa/status/1734981227247981046",
    #          "https://twitter.com/OliLondonTV/status/1736084839181213953",
    #          "https://twitter.com/PalestineNW/status/1735482742295425472",
    #          "https://twitter.com/Resist_05/status/1734343972670337233"]

    # tfile = ['t1.csv', 't2.csv', 't3.csv', 't4.csv', 't5.csv', 't6.csv', 't7.csv', 't8.csv']

    # len1 = len(posts)
    # for i in range(len1):
    #     driver.get(posts[i])
    #     driver.implicitly_wait(10)

    #     time.sleep(5)

    #     tweets = []

    #     try:
    #         all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')
    #         for item in all_tweets:
    #             text_element = item.find_element(By.XPATH, './/div[@lang="en"]')
    #             text = text_element.text.strip()
                
    #             date_element = item.find_element(By.XPATH, './/time')
    #             date = date_element.get_attribute("datetime")
    #             print(text, date)
    #             if text:
    #                 tweets.append([text, date])

    #     except Exception as e:
    #         print(f"Error extracting tweets: {str(e)}")

    #     csv_file_name = tfile[i]

    #     with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
    #         csv_writer = csv.writer(csv_file)
    #         csv_writer.writerows(tweets)

    #     print(f'CSV file "{csv_file_name}" has been created.')