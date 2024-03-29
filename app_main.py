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

                    p{
                      color: #DA1003 !important;
                      font-size:20px !important;
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
        
        full_name="";born="";age="";batting_style="";bowling_style="";playing_role="";relations=""
        for i in details:
            value = i.find_element(By.XPATH,"following-sibling::span").text
            if i.text=="FULL NAME":
                full_name=value
            if i.text=="BORN":
                born=value
            if i.text=="AGE":
                age=value
            if i.text=="BATTING STYLE":
                batting_style=value
            if i.text=="BOWLING STYLE":
                bowling_style=value
            if i.text=="PLAYING ROLE":
                playing_role=value
            if i.text=="RELATIONS":
                relations=value
        
            
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
        driver.close()
            
    def create_dataframes_for_career_stats(self,tables,t):
        headings=[]
        values=[]

        table = tables[t]
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'th')
            for col in cols:
                # if col.text=='':
                #     continue
                headings.append(col.text)
        print(headings)
        print(len(headings))
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            for col in cols:
                values.append(col.text)
        print(values)
        print(len(values))

        overview_df = pd.DataFrame(index=[i for i in range(0,int(len(values)/len(headings)))],columns=headings)
        for k in range(0,int(len(values)/len(headings))):
            for i in range(0,len(headings)):
                overview_df[headings[i]][k]=values[k*len(headings)+i]
        
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


    def recent_matches(self,driver):
        time.sleep(4)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(7)
        tables = driver.find_elements(By.TAG_NAME,'table')
        headings=[]
        values=[]
        head = tables[0].find_element(By.TAG_NAME, 'thead')
        rows = head.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'th')
            for col in cols:
                headings.append(col.text)
        body = tables[0].find_element(By.TAG_NAME, 'tbody')
        rows = body.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            for col in cols:
                values.append(col.text)
        overview_df = pd.DataFrame(index=[i for i in range(0,int(len(values)/len(headings)))],columns=headings)
        for k in range(0,int(len(values)/len(headings))):
            for i in range(0,len(headings)):
                overview_df[headings[i]][k]=values[k*len(headings)+i]
        st.dataframe(overview_df)



    def segregate_allrounders_based_on_gender(self,file_name,cname,lower_limit,upper_limit):
        df = pd.read_csv(file_name)
        female_players=[]
        male_players=[]
        for index,rows in df.iterrows():
            if rows['age']>=lower_limit and rows['age']<=upper_limit:
                print(rows['link'])
                driver = webdriver.Chrome()
                driver.get(rows['link'])
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

                if "Women" in team_names:
                    female_players.append(data)
                else:
                    male_players.append(data)
                driver.close()

        # creating dataframes
        female_df = pd.DataFrame(female_players)
        male_df = pd.DataFrame(male_players)
        
        # dropping duplicates
        female_df.drop_duplicates(inplace=True)
        male_df.drop_duplicates(inplace=True)

        # saving dataframes into csv files
        if file_name==cname+'_allrounders.csv':
            if os.path.exists(cname+"_women_allrounders.csv"):
                female_df.to_csv(cname+"_women_allrounders.csv",mode='a', index=False,header=False)
            else:
                female_df.to_csv(cname+"_women_allrounders.csv",mode='a', index=False,header=True)

            if os.path.exists(cname+"_men_allrounders.csv"):
                male_df.to_csv(cname+"_men_allrounders.csv",mode='a', index=False,header=False)
            else:
                male_df.to_csv(cname+"_men_allrounders.csv",mode='a', index=False,header=True)
        else:
            if os.path.exists(cname+"_women_T20s.csv"):
                female_df.to_csv(cname+"_women_T20s.csv",mode='a', index=False,header=False)
            else:
                female_df.to_csv(cname+"_women_T20s.csv",mode='a', index=False,header=True)

            if os.path.exists(cname+"_men_allrounders.csv"):
                male_df.to_csv(cname+"_men_allrounders.csv",mode='a', index=False,header=False)
            else:
                male_df.to_csv(cname+"_men_allrounders.csv",mode='a', index=False,header=True)

    
    def extract_player_details(self,players,link):
        driver = page.openDriver()
        driver.get(link)
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
        driver.close()
                


    def save_all_player_info(self,file_name,l,h):
        df = pd.read_csv(file_name)
        players=[]
        if file_name == cname+'_allrounders.csv':
            for link in df.link[l:h].to_list():
                self.extract_player_details(players,link)
        elif file_name == cname+'_T20s.csv':
            for link in df.link[l:h].to_list():
                self.extract_player_details(players,link)

        players_df = pd.DataFrame(players)
        players_df.drop_duplicates(inplace=True)
        players_df.fillna("--",inplace=True)

        if file_name == cname+"_allrounders.csv":
            if os.path.exists(cname+"_allrounders_player_info.csv"):
                players_df.to_csv(cname+"_allrounders_player_info.csv",mode='a', index=False,header=False)
            else:
                players_df.to_csv(cname+"_allrounders_player_info.csv",mode='a', index=False,header=True)

        elif file_name == cname+"_T20s.csv":
            if os.path.exists(cname+"_T20s_player_info.csv"):
                players_df.to_csv(cname+"_T20s_player_info.csv",mode='a', index=False,header=False)
            else:
                players_df.to_csv(cname+"_T20s_player_info.csv",mode='a', index=False,header=True)
                

    def get_val(self,table,headings,s):
        values=[]
        for row in table.find_elements(By.TAG_NAME, 'tr'):
                cols = row.find_elements(By.TAG_NAME, 'td')
                for col in cols:
                    values.append(col.text)

        df = pd.DataFrame(index=[i for i in range(0,int(len(values)/len(headings)))],columns=headings)
        for k in range(0,int(len(values)/len(headings))):
            for i in range(0,len(headings)):
                df[headings[i]][k]=values[k*len(headings)+i]

        df[s]=df[s].astype(str).apply(lambda x: x.replace('-','0'))
        df[s]=pd.to_numeric(df[s])    
        val = df[s].sum()
        return val
    
    
    def get_total_runs_wickets(self,headings,headings1,tables):
        total_runs=0;total_wkts=0
        if "Runs" in headings:
            total_runs = self.get_val(tables[0],headings,"Runs")
        elif "Runs" in headings1:
            total_runs = self.get_val(tables[1],headings1,"Runs")
        else:
            total_runs=0

        if "Wkts" in headings:
            total_wkts = self.get_val(tables[0],headings,"Wkts")
        elif "Wkts" in headings1:
            total_wkts = self.get_val(tables[1],headings1,"Wkts")
        else:
            total_wkts=0

        return total_runs,total_wkts
    


    def download_player_runs_wickets(self,file_name):
        df = pd.read_csv(file_name)
        player_data=[]
        for index,rows in df.iterrows():
            driver = webdriver.Chrome()
            driver.get(rows['link'])
            print(rows['link'])
            print(rows['name'])
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(3)

            
            
            tables = driver.find_elements(By.TAG_NAME,'table')

            headings=[];headings1=[]
            for row in tables[0].find_elements(By.TAG_NAME, 'tr'):
                cols = row.find_elements(By.TAG_NAME, 'th')
                for col in cols:
                    headings.append(col.text)  
            print(headings)

            if "MATCH" in headings:
                print("no")
                continue


            for row in tables[1].find_elements(By.TAG_NAME, 'tr'):
                cols = row.find_elements(By.TAG_NAME, 'th')
                for col in cols:
                    headings1.append(col.text)
            print(headings1)

            

            total_runs,total_wkts = self.get_total_runs_wickets(headings,headings1,tables)
            print(total_runs,total_wkts)
           
            data = {
                'Player Name':rows['name'],
                'Runs':total_runs,
                'Wkts':total_wkts
            }
            player_data.append(data)
            driver.close()
            
        
        players_df = pd.DataFrame(player_data)
        print(players_df)
        

        if file_name == cname+"_allrounders.csv":
            if os.path.exists(cname+"_runs_and_wickets_allrounders.csv"):
                players_df.to_csv(cname+"_runs_and_wickets_allrounders.csv",mode='a', index=False,header=False)
            else:
                players_df.to_csv(cname+"_runs_and_wickets_allrounders.csv",mode='a', index=False,header=True)

        elif file_name == cname+"_T20s.csv":
            if os.path.exists(cname+"_runs_and_wickets_T20s.csv"):
                players_df.to_csv(cname+"_runs_and_wickets_T20s.csv",mode='a', index=False,header=False)
            else:
                players_df.to_csv(cname+"_runs_and_wickets_T20s.csv",mode='a', index=False,header=True)   
        

        
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

            if os.path.exists(cname+"_allrounders.csv") and os.path.exists(cname+"_t20s.csv"):
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

                        st.write("Click on this button to get all players data :")
                        if st.button('Download 50 AllRounders'):
                            app.save_all_player_info(cname+'_allrounders.csv',0,50)

                    if option == "T20s": 
                        lower_limit=0
                        upper_limit=0
                        option = st.selectbox(
                                    'Select age',
                                    ('--Select--','15-20','21-22','23-24','25-27','28-29','30-31','32-33','34-36','37-39'))
                        if option != "--Select--":
                            lower_limit=int(option.split('-')[0])
                            upper_limit=int(option.split('-')[1])
                            app.segregate_allrounders_based_on_gender(cname+'_T20s.csv',cname,lower_limit,upper_limit)   
                        app.player_info(cname+'_T20s.csv')

                        st.write("Click on this button to get all players data :")
                        if st.button('Download 50 T20 players'):
                                app.save_all_player_info(cname+'_T20s.csv',0,50)

                        
            
            

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
        if os.path.exists(cname+"_allrounders.csv") and os.path.exists(cname+"_t20s.csv"):  
            option = option_menu(None, ['Select Any Option','AllRounders', 'T20s'],
                                            icons=["pencil","exclamation-diamond"], default_index=0)
            if option == "AllRounders": 
                df = pd.read_csv(cname+"_allrounders.csv")
                if st.button("Download Runs and Wickets for all AllRounders"):
                    app.download_player_runs_wickets(cname+"_allrounders.csv")
                player_names =['--Select--'] + df.name.to_list()
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                selected_player = st.selectbox(
                            "Select a player",
                            options=player_names,
                        )
                if selected_player != '--Select--':
                    st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">Career Statistics of {selected_player}</div>""",unsafe_allow_html=True)
                    link = df['link'][df['name']==selected_player].values[0]
                    driver = page.openDriver()
                    driver.get(link)
                    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                    player_sections = driver.find_elements(By.CSS_SELECTOR,'span.ds-text-tight-m.ds-font-regular.ds-flex')
                    player_section_names = ','.join([section.text for section in player_sections])
                    print(player_section_names)
                    if "Stats" in player_section_names:
                        for i in player_sections:
                            if "Stats" in i.text:
                                time.sleep(5)
                                i.click()
                                break
                        app.career_stats(driver)
                    elif "Matches" in player_section_names:
                        for i in player_sections:
                            if "Matches" in i.text:
                                time.sleep(5)
                                i.click()
                                break
                        app.recent_matches(driver)
                    driver.close()

            if option == "T20s": 
                df = pd.read_csv(cname+"_T20s.csv")
                if st.button("Download Runs and Wickets for all T20 Players"):
                    app.download_player_runs_wickets(cname+"_T20s.csv")
                player_names =['--Select--'] + df.name.to_list()
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                selected_player = st.selectbox(
                            "Select a player",
                            options=player_names,
                        )
                if selected_player != '--Select--':
                    st.markdown(f"""<div style="color: black; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">Career Statistics of {selected_player}</div>""",unsafe_allow_html=True)
                    link = df['link'][df['name']==selected_player].values[0]
                    driver = page.openDriver()
                    driver.get(link)
                    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                    player_sections = driver.find_elements(By.CSS_SELECTOR,'span.ds-text-tight-m.ds-font-regular.ds-flex')
                    player_section_names = ','.join([section.text for section in player_sections])
                    print(player_section_names)
                    if "Stats" in player_section_names:
                        for i in player_sections:
                            if "Stats" in i.text:
                                time.sleep(5)
                                i.click()
                                break
                        app.career_stats(driver)
                    elif "Matches" in player_section_names:
                        for i in player_sections:
                            if "Matches" in i.text:
                                time.sleep(5)
                                i.click()
                                break
                        app.recent_matches(driver)
                    driver.close()
                
        else:
            st.write('Kindly go to "Player Info" tab and click on AllRounders and T20s players button in order to get career statistics of each player')
            
    
    
    

    
    

    
    
    
    