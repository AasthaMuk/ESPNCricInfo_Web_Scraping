# Importing Libraries
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import streamlit as st


# Main method
if __name__=="__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get("https://www.espncricinfo.com/cricketers/team/india-6")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    # Wait for images to load
    # wait = WebDriverWait(driver, 9000)
    # images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.ds-block")))
    # images = driver.find_elements(By.CSS_SELECTOR, "img.ds-block")
    
    player_names = driver.find_elements(By.CSS_SELECTOR, "span.ds-text-tight-l")
    age = driver.find_elements(By.CSS_SELECTOR, "span.ds-text-tight-m.ds-font-regular.ds-text-typo-mid3")

    
    players = [i.text for i in player_names]
    ages = [i.text.split("y")[0] for i in age]

    player_info={'name':players, 'age':ages}
    print(player_info)

    pd.DataFrame(player_info).to_csv('player_info.csv')

    # print(len(images))
    # print(len(player_names))
    # print(len(age))
    # for i in range(len(player_names)):
    #     print(player_names[i].text)
 
    # for i in range(len(age)):
    #     print(age[i].text)
    # print(player_names[0].text)
    # print(type(images))
        
    # for i in range(len(images)):
    #     print(images[i].get_attribute("alt")+" "+images[i].get_attribute("src"))
    #     # print(images[i].get_attribute("src"))

    
    # driver.find_element(By.NAME, "q").send_keys("selenium")
    # driver.find_element(By.NAME, "q").send_keys(Keys.ENTER)