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
import os
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

# Class "Settings" contains all the styles and settings for the streamlit page
class Settings:
    def __init__(self) -> None:
        pass

    def openDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver
    
    def set_page_config(self):
        icon = Image.open("images/icon.png")
        st.set_page_config(page_title= "CricBuzz",
                        page_icon= icon,
                        layout= "wide",)
        st.markdown("<h1 style='text-align: left; color: black; font-size:70px;'>Cric Mania is ON!!</h1>", unsafe_allow_html=True)
        st.markdown(""" 
            <style>
                    .stApp,[data-testid="stHeader"] {
                        background: url("https://t4.ftcdn.net/jpg/05/86/41/69/240_F_586416971_vPk0urf9UkQLpFdAFW3LfQMAVnwNlEWv.jpg");
                        background-size: cover
                    }

                    #custom-container {
                        background-color: white !important;
                        border-radius: 10px; /* Rounded corners */
                        margin: 20px; /* Margin */
                        padding: 20px;
                    }
            </style>""",unsafe_allow_html=True)



# Class "App" contains all utility methods to extract player data from ESPNCricInfo website
class GetPlayers:
    def __init__(self):
        pass

    def get_allrounders(self,driver,cname):
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
            try:
                s = i.text.split("Age: ")[1]
                year = int(s.split("y")[0])
                d = int(s.split("y")[1].split("d")[0])
                if d<365:
                    day = d
                else:
                    day = d-365
                    year+=1
                print(year)
            except:
                year=None
            ages.append(year)
        players_info={'name':names, 'age':ages,'link':links}
        pd.DataFrame(players_info).to_csv(cname+'_allrounders.csv',index=False)


    def get_t20s(self,driver,cname):
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
            try:
                s = i.text.split("Age: ")[1]
                year = int(s.split("y")[0])
                d = int(s.split("y")[1].split("d")[0])
                if d<365:
                    day = d
                else:
                    day = d-365
                    year+=1
            except:
                year=None
            ages.append(year)

        players_info={'name':names, 'age':ages,'link':links}
        pd.DataFrame(players_info).to_csv(cname+'_T20s.csv',index=False)

    def preprocessing(self,file_name):
        print('file received : '+file_name)
        df = pd.read_csv(file_name)
        # dropping null values
        df['age']=df.age.fillna(df.age.mode()[0])
        # dropping duplicates
        df.drop_duplicates(inplace=True)
        # changing the type of "age" column
        df['age']=df['age'].astype(int)
        # removing row with age>=40
        df = df[df['age'] < 40]
        return df
    
    def get_url(self,cname):
        if cname=="india":
            return f"https://www.espncricinfo.com/cricketers/team/{cname}-6"
        elif cname=="england":
            return f"https://www.espncricinfo.com/cricketers/team/{cname}-1"
        elif cname=="bangladesh":
            return f"https://www.espncricinfo.com/cricketers/team/{cname}-25"
        elif cname=="australia":
            return f"https://www.espncricinfo.com/cricketers/team/{cname}-2"
        elif cname=="new-zealand":
            return f"https://www.espncricinfo.com/cricketers/team/{cname}-5"
        
    
    def get_country(self,cname,page):
        if st.button('Get All Rounders for '+cname):
                driver = page.openDriver()
                driver.get(app.get_url(cname))                    
                driver.find_element(By.XPATH, '//span[contains(text(), "Allrounders")]').click()
                app.get_allrounders(driver,cname)
                file_name=cname+'_allrounders.csv'
                print(file_name)
                df =self.preprocessing(file_name)
                pd.DataFrame(df).to_csv(cname+'_allrounders.csv',index=False)

        if st.button('Get T20s for '+cname):
                driver = page.openDriver()
                driver.get(app.get_url(cname)) 
                driver.find_element(By.XPATH, '//span[contains(text(), "T20s")]').click()
                app.get_t20s(driver,cname)
                file_name=cname+'_T20s.csv'
                print(file_name)
                df = self.preprocessing(file_name)
                pd.DataFrame(df).to_csv(cname+'_T20s.csv',index=False)


    def player_info(self,file_name):
        df = pd.read_csv(file_name)
        player_names =['--Select--'] + df.name.to_list()
        selected_player = st.selectbox(
            "Select a player",
            options=player_names,
        )

        if selected_player == '--Select--':
            return
        link = df['link'][df['name']==selected_player].values[0]
        driver = page.openDriver()
        driver.get(link)
        
        
        # Your CSS selector for the elements you want to retrieve
        try:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(10)
            image_link = driver.find_element(By.CSS_SELECTOR,'div.ds-ml-auto.ds-w-48.ds-h-48>div>img').get_attribute('src')
        except: image_link = "https://wassets.hscicdn.com/static/images/player-jersey.svg"
        print(image_link)
                
        # full_name = driver.find_element(By.CSS_SELECTOR, 'div.ds-col-span-2.lg\:ds-col-span-1>span>p').text
        player_details = driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-title-s.ds-font-bold.ds-text-typo')
        try:
            full_name = player_details[0].text
            born = player_details[1].text
            age = player_details[2].text
            batting_style = player_details[3].text
            bowling_style = player_details[4].text
            playing_role =  player_details[5].text
            relations = driver.find_element(By.CSS_SELECTOR,'div.ds-flex.ds-flex-wrap>span>div>a>span').text + driver.find_element(By.CSS_SELECTOR,'div.ds-flex.ds-flex-wrap>span>p').text
        except:
            relations="--"

        teams = driver.find_elements(By.CSS_SELECTOR,'div.ds-grid.lg\:ds-grid-cols-3.ds-grid-cols-2.ds-gap-y-4>a>span')
        team_names = ', '.join([team.text for team in teams])
            
        st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">Player Info:</div>""",unsafe_allow_html=True)
        col1,col2 = st.columns([1,3])
        with col1:
            st.image(image_link, width=250)
        with col2:
            st.markdown(f"""<div id="custom-container">
                            <p>Name : {full_name}</p>
                            <p>Born in : {born}</p>
                            <p>Age : {age}</p>
                            <p>Batting Style : {batting_style}</p>
                            <p>Bowling Style : {bowling_style}</p>
                            <p>Playing Role : {playing_role}</p>
                            <p>Teams played : {team_names}</p>
                            <p>Relations : {relations}</p>
                            </div>""",unsafe_allow_html=True)
            
    def create_dataframes_for_career_stats(self,tables,t):
        headings=[]
        values=[]

        table = tables[t]
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'th')
            for col in cols:
                if col.text=='':
                    continue
                headings.append(col.text)
        print(headings)
        print(len(headings))
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            for col in cols:
                values.append(col.text)
        print(values)
        print(len(values))
        
        overview_df = pd.DataFrame(index=[values[0]],columns=headings)
        for i in range(0,len(headings)):
            overview_df[headings[i]]=values[i+1]
        st.dataframe(overview_df)

        
    def career_stats(self,driver):
        time.sleep(3)
        column =driver.find_element(By.CSS_SELECTOR,'div.ds-flex.ds-items-center.ds-space-x-4')
    
        subcolumns = column.find_elements(By.XPATH,"//div[@class='ds-w-[160px]']")
        for i in subcolumns:
            header = i.find_element(By.CSS_SELECTOR, 'div.ds-popper-wrapper>div>span').click()
            options = driver.find_elements(By.CSS_SELECTOR,'li.ds-w-full.ds-flex>div>span')
            for j in options:
                if j.text=="Allround":
                    j.click()
                    break
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(7)
        tables = driver.find_elements(By.TAG_NAME,'table')
        app.create_dataframes_for_career_stats(tables,0)
        app.create_dataframes_for_career_stats(tables,1)
        
        # print(tables)

        
        

    def segregate_allrounders_based_on_gender(self,file_name,cname,lower_limit,upper_limit):
        df = pd.read_csv(file_name)
        female_players=[]
        male_players=[]
        male_data= {'Brand':[],'Description':[],'Discountprice':[],
           'Actualprice':[],'Discountpercent':[],'Links':[],'ImageLinks':[]}
        for index,rows in df.iterrows():
            if rows['age']>=lower_limit and rows['age']<=upper_limit:
                print(rows['link'])
                driver = webdriver.Chrome()
                driver.get(rows['link'])
                player_details = driver.find_elements(By.CSS_SELECTOR, 'span.ds-text-title-s.ds-font-bold.ds-text-typo')
                try:
                    full_name = player_details[0].text
                    born = player_details[1].text
                    age = player_details[2].text
                    batting_style = player_details[3].text
                    bowling_style = player_details[4].text
                    playing_role =  player_details[5].text
                    relations = driver.find_element(By.CSS_SELECTOR,'div.ds-flex.ds-flex-wrap>span>div>a>span').text + driver.find_element(By.CSS_SELECTOR,'div.ds-flex.ds-flex-wrap>span>p').text
                except:
                    relations="--"

                teams = driver.find_elements(By.CSS_SELECTOR,'div.ds-grid.lg\:ds-grid-cols-3.ds-grid-cols-2.ds-gap-y-4>a>span')
                team_names = ', '.join([team.text for team in teams])

                if "Women" in team_names:
                    data = {'Full Name':full_name,'Born':born,'Age':age,'Batting Style':batting_style,'Bowling Style':bowling_style,'Playing Role':playing_role,'Teams played':team_names,'Relations':relations}
                    female_players.append(data)
                else:
                    data = {'Full Name':full_name,'Born':born,'Age':age,'Batting Style':batting_style,'Bowling Style':bowling_style,'Playing Role':playing_role,'Teams played':team_names,'Relations':relations}
                    male_players.append(data)
                driver.close()

       




        # creating dataframes
        female_df = pd.DataFrame(female_players)
        male_df = pd.DataFrame(male_players)
        
        # dropping duplicates
        female_df.drop_duplicates(inplace=True)
        male_df.drop_duplicates(inplace=True)

        # saving dataframes into csv files
        if os.path.exists(cname+"_women_allrounders.csv"):
            female_df.to_csv(cname+"_women_allrounders.csv",mode='a', index=False,header=False)
        else:
            female_df.to_csv(cname+"_women_allrounders.csv",mode='a', index=False,header=True)

        if os.path.exists(cname+"_men_allrounders.csv"):
            male_df.to_csv(cname+"_men_allrounders.csv",mode='a', index=False,header=False)
        else:
            male_df.to_csv(cname+"_men_allrounders.csv",mode='a', index=False,header=True)
        

    

        
        
        

        
# Main method
if __name__=="__main__":
    page = Settings()
    page.set_page_config()

    
    with st.sidebar:
        selected = option_menu("Menu", ["Home","Players Info","Career Stats"], 
                    icons=["house","graph-up-arrow","bar-chart-line"],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#B1A3F7"}})
    if selected=="Home":
        col1,col2=st.columns([3,1])
        with col1:
            st.write(" ")
            st.write(" ")
            st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">ESPN Cric Info :</div>""",unsafe_allow_html=True)
            
            st.markdown(f"""<div id="custom-container">ESPNcricinfo is the world's leading cricket website and among the top five single-sport websites in the world.
            Founded in 1993, ESPNcricinfo's content includes news, live ball-by-ball coverage of all Test and one-day international matches and features written by some of the world's best cricketers and cricket writers. The site also includes in-depth statistics on every one of the 3000 international and 50,000 first-class cricketers to have played the game.
            Now a wholly owned subsidiary of ESPN Inc., the world's leading multimedia sports entertainment company, ESPNcricinfo is available to cricket fans through the online media and on a host of mobile platforms and handheld devices.
            ESPNcricinfo has a thriving user community and reaches over 20 million users every month.</div>""",unsafe_allow_html=True)
            
            st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">About this app :</div>""",unsafe_allow_html=True)
            st.markdown(f"""<div id="custom-container"> This app is developed by Me that extracts the details of players who are allrounders and t20s players. Also, it shows the career statistics of each player.</div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold; text-align:left;">Source ⬇️</div>""",unsafe_allow_html=True)
            st.write("https://www.espncricinfo.com/")
        with col2:
            st.image("images/image2.jpg")   
            st.image("images/images.jpg")  
            st.image("images/image1.jpg")
    if selected=="Players Info":
        app = GetPlayers()
        tab1,tab2,tab3,tab4,tab5 = st.tabs(["India", "England", "Bangladesh","Australia","New Zealand"])
        
        with tab1:
            cname="india"
            app.get_country(cname,page)
            option = option_menu(None, ['Select Any Option','AllRounders', 'T20s'],
                                    icons=["pencil","exclamation-diamond"], default_index=0)
            if option == "AllRounders": 
                lower_limit=0
                upper_limit=0
                option = st.selectbox(
                            'Select age',
                            ('--Select--','15-20','21-22','23-24','25-27','28-29','30-31','32-33','34-36','37-39'))
                if option != "--Select--":
                    lower_limit=int(option.split('-')[0])
                    upper_limit=int(option.split('-')[1])
                    app.segregate_allrounders_based_on_gender(cname+'_allrounders.csv',cname,lower_limit,upper_limit)
                
                app.player_info(cname+'_allrounders.csv')

            if option == "T20s":    
                app.player_info(cname+'_T20s.csv')
   
        with tab2:
            app.get_country("england",page)
        with tab3:
            app.get_country("bangladesh",page)
        with tab4:
            app.get_country("australia",page)
        with tab5:
            app.get_country("new-zealand",page)

    if selected=="Career Stats":
        app = GetPlayers()
        cname="india"
            
        option = option_menu(None, ['Select Any Option','AllRounders', 'T20s'],
                                        icons=["pencil","exclamation-diamond"], default_index=0)
        if option == "AllRounders": 
            df = pd.read_csv(cname+"_allrounders.csv")
            player_names =['--Select--'] + df.name.to_list()
            selected_player = st.selectbox(
                        "Select a player",
                        options=player_names,
                    )

            if selected_player != '--Select--':
                link = df['link'][df['name']==selected_player].values[0]
                driver = page.openDriver()
                driver.get(link)
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                player_sections = driver.find_elements(By.CSS_SELECTOR,'span.ds-text-tight-m.ds-font-regular.ds-flex')
                player_section_names = ','.join([section.text for section in player_sections])
                print(player_section_names)
                if "Stats" in player_section_names:
                    for i in player_sections:
                        if "Stats" in i.text:
                            i.click()
                            break
                    app.career_stats(driver)
                else:
                    print("no")
                driver.close()

                

            
    # with tab6:
    #     app.get_country()
    # with tab7:
    #     app.get_country()
    # with tab8:
    #     app.get_country()
    # with tab9:
    #     app.get_country()

    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    # Wait for images to load
    # wait = WebDriverWait(driver, 9000)
    # images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.ds-block")))
    # images = driver.find_elements(By.CSS_SELECTOR, "img.ds-block")
    
    

    
    

    
    
    
    