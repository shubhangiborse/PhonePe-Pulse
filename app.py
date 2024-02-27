import pandas as pd
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image

icon = Image.open(r"./phonepe-icon.png")

st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                   )


st.sidebar.header("**PhonePe Pulse Analysis**")

connection_string = "mysql+mysqlconnector://root:borse123@127.0.0.1:3306/phonepe"

conn = st.connection(
    "local_db",
    type="sql",
    url=connection_string
)

with st.sidebar:
    selected = option_menu("Menu", ["Home","Analysis","About Me"], 
                icons=["house","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#b0c8ef"},
                        "nav-link-selected": {"background-color": "#16a535"}})
    

# MENU 1 - HOME
if selected == "Home":
    st.image("./phonepe-icon.png", "PhonePe Pulse", width=100)

    st.markdown("# Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly]")
    st.markdown("## Technologies : Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly")
    
# MENU 1.A - HOME:About me
if selected == "About Me":
    st.image("./phonepe-icon.png", "PhonePe Pulse", width=100)

    st.markdown("# Dr. Shubhangi Borse")
    st.markdown("## Research Analyst")
    st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/dr-shubhangi-borse-48990565/)") 
    st.markdown("[![Github](https://img.icons8.com/material-outlined/48/000000/github.png)](https://github.com/shubhangiborse)") 
    st.markdown("[![Medium](https://static-00.iconduck.com/assets.00/medium-icon-256x256-sszkhuhr.png)](https://medium.com/@drshubhangi)") 
    

if selected == "Analysis":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    
    
    option = st.selectbox(
        "Question?",
        ("Top 10 Aggregated Transaction Count", "Top 10 Mobile phone Brands",  "Aggregated Transaction Amount in Map View", "Aggregated Transaction Count in Map View", 
         "Aggregated Transaction Type", "Aggregated Total Users by State Map View", 
         "Transaction Count Growth", "Transaction Amount Growth","Registered Users Growth","Device Brand Growth in all over India"),
        placeholder="Select the analysis ",
        )
    if option == "Top 10 Aggregated Transaction Count":
        df  = conn.query(f"select state as State, sum(Transaction_count) as Transactions_Count, sum(Transaction_amount) as Total_Amount from transaction where year = {Year} and Quater = {Quarter} group by State order by Total_Amount desc limit 10")
       

        fig = px.pie(df, values='Total_Amount',
                            names='State',
                            title='Top 10 Aggregated Transaction Amount',
                            color_discrete_sequence=px.colors.sequential.BuGn_r,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count':'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
        
        st.dataframe(df)
    
    if option == "Top 10 Mobile phone Brands":
        df  = conn.query(f"select Device_brand as Brand, sum(Device_count) as Total_Users, avg(Device_percentage)*100 as Avg_Percentage from user where year = {Year} and Quater = {Quarter} group by Device_brand order by Total_Users desc limit 10")
        if df.empty:
            st.markdown("### There is no data in this range")
        else:
            
            fig = px.bar(df,
                            title='Top 10 mobile handset',
                            x="Brand",
                            y="Total_Users", 
                            orientation='v',
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Oranges,
                            labels={"Avg_Percentage": "Avg_Percentage"})

            st.plotly_chart(fig,use_container_width=True) 
            st.dataframe(df)
        

    if option == "Aggregated Transaction Amount in Map View":
        df1  = conn.query(f"select state as State, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from transaction where year = {Year} and Quater = {Quarter} group by state order by state")
        df2 = pd.read_csv(r'statename.csv')
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_amount',
                    color_continuous_scale='oranges')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
    if option == "Aggregated Transaction Count in Map View":
        df1  = conn.query(f"select state as State, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from transaction where year = {Year} and Quater = {Quarter} group by state order by state")
        df2 = pd.read_csv(r'statename.csv')
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale='oranges')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
    if option == "Aggregated Transaction Type":
        df  = conn.query(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from transaction where year= {Year} and Quater = {Quarter} group by Transaction_type order by Transaction_type")
        # df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
    if option == "Aggregated Total Users by State Map View":
        df1  = conn.query(f"select state as State, sum(Registered_users) as Total_Users, sum(AppOpens) as Total_Appopens from user where year = {Year} and Quater = {Quarter} group by State order by State")

        if df1.empty:
            st.markdown("### There is no data in this range")
        else:
            df2 = pd.read_csv(r'statename.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Users',
                        color_continuous_scale='oranges')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
    if option == "Transaction Count Growth":
        st.markdown("#### :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        
        df  = conn.query(f"select Year, Quater, CONCAT(Year,' Q',Quater) as Time, sum(Transaction_count) as Transactions_Count, sum(Transaction_amount) as Total_Amount from transaction where State = '{selected_state}' group by Year, Quater order by Year")
        fig = px.line(df,
                     title='Transaction Count Growth',
                     x="Time",
                     y="Transactions_Count",
                     orientation='v'
                     )
        st.plotly_chart(fig,use_container_width=False)
        
    if option == "Transaction Amount Growth":
        st.markdown("#### :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        
        df  = conn.query(f"select Year, Quater, CONCAT(Year,' Q',Quater) as Time, sum(Transaction_count) as Transactions_Count, sum(Transaction_amount) as Total_Amount from transaction where State = '{selected_state}' group by Year, Quater order by Year")
        fig = px.line(df,
                     title='Transaction Count Growth',
                     x="Time",
                     y="Total_Amount",
                     orientation='v'
                     )
        st.plotly_chart(fig,use_container_width=False)
        
    if option == "Registered Users Growth":
        st.markdown("#### :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        
        df  = conn.query(f"select Year, Quater, CONCAT(Year,' Q',Quater) as Time, sum(Registered_users) as Users_Count from user where State = '{selected_state}' group by Year, Quater order by Year")
        fig = px.line(df,
                     title='Transaction Count Growth',
                     x="Time",
                     y="Users_Count",
                     orientation='v'
                     )
        st.plotly_chart(fig,use_container_width=False)
        
        
    if option == "Device Brand Growth in all over India":
        st.markdown("#### :red[Select any Brand to explore more]")
        selected_brand = st.selectbox("",
                             ('Vivo','Xiaomi','Samsung','Realme','Oppo','OnePlus','Tecno','Apple','Huawei','Motorola','Others','Lenovo','Gionee','COOLPAD','HMD Global','Lyf','Micromax','Asus','Infinix','Lava'))
        
        
        df  = conn.query(f"select Year, Quater, CONCAT(Year,' Q',Quater) as Time, sum(Device_count) as Device_Count from user where Device_brand = '{selected_brand}' group by Year, Quater order by Year")
        if df.empty:
            st.markdown("### There is no data")
        else:
            fig = px.line(df,
                        title='Transaction Count Growth',
                        x="Time",
                        y="Device_Count",
                        orientation='v'
                        )
            st.plotly_chart(fig,use_container_width=False)
            
        

# st.write('You selected:', option)

    
