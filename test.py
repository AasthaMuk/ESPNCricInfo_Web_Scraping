# Importing Libraries
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import streamlit as st
import time
import os

# Main method
if __name__=="__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get("https://www.espncricinfo.com/cricketers/d-avinash-1119009")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    
    time.sleep(3)
    details =driver.find_elements(By.CSS_SELECTOR,'p.ds-text-tight-m.ds-font-regular.ds-uppercase.ds-text-typo-mid3')
    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(10)
        image_link = driver.find_element(By.CSS_SELECTOR,'div.ds-ml-auto.ds-w-48.ds-h-48>div>img').get_attribute('src')
    except: image_link = "https://wassets.hscicdn.com/static/images/player-jersey.svg"

    teams = driver.find_elements(By.CSS_SELECTOR,'div.ds-grid.lg\:ds-grid-cols-3.ds-grid-cols-2.ds-gap-y-4>a>span')
    team_names = ', '.join([team.text for team in teams])

    data={'FULL NAME':'','BORN':'','AGE':'','BATTING STYLE':'','BOWLING STYLE':'','PLAYING ROLE':'','TEAMS PLAYED':team_names,'RELATIONS':'','IMAGE LINK':image_link}
    players=[]

    for i in details:
        value = i.find_element(By.XPATH,"following-sibling::span").text
        if i.text=="FULL NAME":
            data['FULL NAME']=value
        if i.text=="BORN":
            data['BORN']=value
        if i.text=="AGE":
            data['AGE']=value
        if i.text=="BATTING STYLE":
            data['BATTING STYLE']=value
        if i.text=="BOWLING STYLE":
            data['BOWLING STYLE']=value
        if i.text=="PLAYING ROLE":
            data['PLAYING ROLE']=value
        if i.text=="RELATIONS":
            data['RELATIONS'] = value
        
    
    players.append(data)
    players_df = pd.DataFrame(players)
    print(players_df)
    if os.path.exists("test.csv"):
        players_df.to_csv("test.csv",mode='a', index=False,header=False)
    else:
        players_df.to_csv("test.csv",mode='a', index=False,header=True)
    # print(d)
    