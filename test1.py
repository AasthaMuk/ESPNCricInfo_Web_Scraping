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

    driver.get("https://www.espncricinfo.com/cricketers/akash-deep-1176959")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    
    time.sleep(3)
    headings=[];values=[]
    tables = driver.find_elements(By.TAG_NAME,'table')
    rows = tables[0].find_elements(By.TAG_NAME, 'tr')
    for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'th')
            for col in cols:
                headings.append(col.text)
    # print(headings)
    # print(len(headings))

    for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            for col in cols:
                values.append(col.text)
    # print(values)
    # print(len(values))

    overview_df = pd.DataFrame(index=[i for i in range(0,int(len(values)/len(headings)))],columns=headings)
    
    for k in range(0,int(len(values)/len(headings))):
            for i in range(0,len(headings)):
                overview_df[headings[i]][k]=values[k*len(headings)+i]

    overview_df['Wkts']=pd.to_numeric(overview_df['Wkts'])    
    total_wkts = overview_df['Wkts'].sum()
    print(total_wkts)

    headings=[];values=[]
    rows = tables[1].find_elements(By.TAG_NAME, 'tr')
    for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'th')
            for col in cols:
                headings.append(col.text)
    # print(headings)
    # print(len(headings))

    for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            for col in cols:
                values.append(col.text)
    # print(values)
    # print(len(values))

    over_df = pd.DataFrame(index=[i for i in range(0,int(len(values)/len(headings)))],columns=headings)
    
    for k in range(0,int(len(values)/len(headings))):
            for i in range(0,len(headings)):
                over_df[headings[i]][k]=values[k*len(headings)+i]

    over_df['Runs']=pd.to_numeric(over_df['Runs']) 
    total_runs = over_df['Runs'].sum()
    print(total_runs)
    
    