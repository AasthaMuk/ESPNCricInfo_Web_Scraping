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

# Main method
if __name__=="__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get("https://www.espncricinfo.com/cricketers/akash-deep-1176959/matches")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    
    # time.sleep(3)
    # column =driver.find_element(By.CSS_SELECTOR,'div.ds-flex.ds-items-center.ds-space-x-4')
    
    # subcolumns = column.find_elements(By.XPATH,"//div[@class='ds-w-[160px]']")
    # for i in subcolumns:
    #     header = i.find_element(By.CSS_SELECTOR, 'div.ds-popper-wrapper>div>span').click()
    #     options = driver.find_elements(By.CSS_SELECTOR,'li.ds-w-full.ds-flex>div>span')
    #     for j in options:
    #         if j.text=="Allround":
    #             j.click()
    #             break
    time.sleep(10)
    tables = driver.find_elements(By.TAG_NAME,'table')
    print(len(tables))

    headings=[]
    values=[]

    # table = tables[0]
    
    head = tables[0].find_element(By.TAG_NAME, 'thead')
    rows = head.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'th')
        for col in cols:
            headings.append(col.text) #print(col.text)
    
    body = tables[0].find_element(By.TAG_NAME, 'tbody')
    rows = body.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        for col in cols:
            values.append(col.text)
    print(values)
    # print(headings)
    print(len(headings))
    
    # for row in rows:
    #     cols = row.find_elements(By.TAG_NAME, 'td')
    #     for col in cols:
    #         values.append(col.text)
    # print(values)
    print(len(values))
    
    overview_df = pd.DataFrame(index=[i for i in range(0,int(len(values)/len(headings)))],columns=headings)
    for k in range(0,int(len(values)/len(headings))):
        for i in range(0,len(headings)):
            overview_df[headings[i]][k]=values[k*len(headings)+i]
    
        
    print(overview_df)

    # df=pd.DataFrame({'Overview':['2016-2018',18,15,2,303,50,23.30,382,79.31,0,1,0,25,7]}) 
    
    
    
    
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    # Wait for images to load
    # wait = WebDriverWait(driver, 9000)
    # images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.ds-block")))
    # images = driver.find_elements(By.CSS_SELECTOR, "img.ds-block")
    
    # player_names = driver.find_elements(By.CSS_SELECTOR, "span.ds-text-tight-l")
    # age = driver.find_elements(By.CSS_SELECTOR, "span.ds-text-tight-m.ds-font-regular.ds-text-typo-mid3")

    
    # players = [i.text for i in player_names]
    # ages = [i.text.split("y")[0] for i in age]

    # player_info={'name':players, 'age':ages}
    # print(player_info)

    # pd.DataFrame(player_info).to_csv('player_info.csv')

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