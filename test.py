

# s = "Age: 23y 369d".split("Age: ")[1]
# year = int(s.split("y")[0])
# d = int(s.split("y")[1].split("d")[0])
# if d<365:
#     day = d
# else:
#     day = d-365
#     year+=1
# print(year)

import pandas as pd
import numpy as np
import streamlit as st



# Use st.markdown to insert custom HTML and CSS
st.markdown(
    """
    <style>
        .main {
            width: 99.75%;
            float: left;
        }
        .stsidebar {
            width: 0.25%;
            float: right;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Your main content goes here
st.markdown("<div class='main'>Main Content</div>", unsafe_allow_html=True)

# Your sidebar content goes here
st.markdown("<div class='sidebar'>Sidebar Content</div>", unsafe_allow_html=True)

# df = pd.read_csv('india_allrounders.csv')

# option = st.selectbox(
#                         'Select age',
#                         ('--Select--','15-20','21-22','23-24','25-27','28-29','30-31','32-33','34-36','37-39'))

# print(option)
# print(type(option))
# if option != "--Select--":
#     lower_limit=int(option.split('-')[0])
#     print(lower_limit)
# upper_limit=int(option.split('-')[1])

# for index,rows in df.iterrows():
#     if rows['age']>=15 and rows['age']<=20:
#         print(rows['link'])

# df['age']=df.age.fillna(df.age.mode()[0])
# # df['age']=df[np.mean(df['age']).astype(int)]

# print(df['age'][:50])
# # print(df[df['name']=='D Avinash'])

