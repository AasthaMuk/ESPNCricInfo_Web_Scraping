# Importing Libraries
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

class GetPlayers:
    def __init__(self):
        pass

    def get_allrounders(self,driver):
        driver.get("https://www.espncricinfo.com/cricketers/team/india-6")
        driver.find_element(By.XPATH, '//span[contains(text(), "Allrounders")]').click()
        names=[]
        ages=[]
        links=[]
        # Scroll down to trigger lazy loading
        while True:
            # Your CSS selector for the elements you want to retrieve
            player_names = driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-tight-l')
            age = driver.find_elements(By.CSS_SELECTOR, "span.ds-text-tight-m.ds-font-regular.ds-text-typo-mid3")
            link = driver.find_elements(By.CSS_SELECTOR, 'div.ds-popper-wrapper.ds-inline>a.ds-flex')

            # Scroll down using JavaScript to trigger lazy loading
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Add a wait to allow time for lazy loading to occur
            time.sleep(2)

            # Break the loop if no more content is loaded
            if len(driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-tight-l')) == len(player_names):
                break

            # Break the loop if no more content is loaded
            if len(driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-tight-m.ds-font-regular.ds-text-typo-mid3')) == len(age):
                break

            # Break the loop if no more content is loaded
            if len(driver.find_elements(By.CSS_SELECTOR, 'div.ds-popper-wrapper.ds-inline>a.ds-flex')) == len(link):
                break

        

        for i in link:
            pattern = r'https://www\.espncricinfo\.com/cricketers/[a-zA-Z0-9-]+-\d+'
            if re.match(pattern, str(i.get_attribute('href'))):
                links.append(i.get_attribute('href'))

        for i in player_names:
            names.append(i.text)

        for i in age:
            ages.append(i.text)
        # print(len(ages))
        # print(ages)

        players_info={'name':names, 'age':ages,'link':links}
        # print(players_info)

        for i in players_info.keys():
            print(i,len(players_info[i]))

        pd.DataFrame(players_info).to_csv('player_info_allrounders.csv',index=False)

    def get_t20s(self,driver):
        driver.get("https://www.espncricinfo.com/cricketers/team/india-6")
        driver.find_element(By.XPATH, '//span[contains(text(), "T20s")]').click()
        names=[]
        ages=[]
        links=[]
        # Scroll down to trigger lazy loading
        while True:
            # Your CSS selector for the elements you want to retrieve
            player_names = driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-tight-l')
            age = driver.find_elements(By.CSS_SELECTOR, "span.ds-text-tight-m.ds-font-regular.ds-text-typo-mid3")
            link = driver.find_elements(By.CSS_SELECTOR, 'div.ds-popper-wrapper.ds-inline>a.ds-flex')

            # Scroll down using JavaScript to trigger lazy loading
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Add a wait to allow time for lazy loading to occur
            time.sleep(2)

            # Break the loop if no more content is loaded
            if len(driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-tight-l')) == len(player_names):
                break

            # Break the loop if no more content is loaded
            if len(driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-tight-m.ds-font-regular.ds-text-typo-mid3')) == len(age):
                break

            # Break the loop if no more content is loaded
            if len(driver.find_elements(By.CSS_SELECTOR, 'div.ds-popper-wrapper.ds-inline>a.ds-flex')) == len(link):
                break

        

        for i in link:
            pattern = r'https://www\.espncricinfo\.com/cricketers/[a-zA-Z0-9-]+-\d+'
            if re.match(pattern, str(i.get_attribute('href'))):
                links.append(i.get_attribute('href'))

        for i in player_names:
            names.append(i.text)

        for i in age:
            ages.append(i.text)
        # print(len(ages))
        # print(ages)

        players_info={'name':names, 'age':ages,'link':links}
        # print(players_info)

        for i in players_info.keys():
            print(i,len(players_info[i]))

        pd.DataFrame(players_info).to_csv('player_info_T20s.csv',index=False)



# Main method
if __name__=="__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    app = GetPlayers()
    app.get_allrounders(driver)
    app.get_t20s(driver)

    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    # Wait for images to load
    # wait = WebDriverWait(driver, 9000)
    # images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.ds-block")))
    # images = driver.find_elements(By.CSS_SELECTOR, "img.ds-block")
    
    

    
    

    
    
    
    