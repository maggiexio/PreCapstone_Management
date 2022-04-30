import streamlit as st
import pandas as pd
import plotly 
import plotly.express as px
     
@st.cache
def raw_data(input_file, sheetname):
  df=pd.read_excel(open(input_file, 'rb'), sheet_name=sheetname )
  return df

#######################glabal variables

#define functions

##############################
st.set_page_config(layout="wide", initial_sidebar_state="auto")
col11, col12 = st.columns((3,1))
with col11:
  title_1="Zullee Data Exploration"
  st.markdown(f'<h1 style="text-align: center;color: green;">{title_1}</h1>',unsafe_allow_html=True)
  subj_1="-- Pre-CapStone project"
  st.markdown(f'<h2 style="text-align: center;color: green;">{subj_1}</h2>',unsafe_allow_html=True) 
  st.markdown ("Team 6: profit model")
  st.markdown("Data file includes net sales and number of orders/gusts, break down to every hour and  every weekday from Jan 2022 to Marchh 2022 at Spokane. ")
   
with col12:
  title_11="Hello! I am Alexa. Can I help you?"
  st.markdown(f'<h2 style="text-align: center;color: purple;">{title_11}</h2>',unsafe_allow_html=True)
  user_input =''
  user_input = st.text_area("Type your questions here (enter 'contrl+enter' to finish your questions)", value="", max_chars=5000)
  if user_input.lower().find('no question') != -1:
    st.write ("Great! Have a nice day!")
  else:
    if user_input.lower().find('item level plots') != -1:
      st.write ("At this point, only Spokane data are provided.")
    else: 
      if user_input.lower()!='': 
        st.write ("Sorry, I am not sure! Please contact xix294@g.harvard.edu")
         
# read in data
df_ori=raw_data("./data/Sales Summary 123 2022 - Spokane - Python.xlsx", "Hourly Breakdown")
df_ori['NetSale_group']=""
df_ori['OrderN_group']=""
df_ori['GuestN_group']=""
bin_OrderN= [0,100,200,300,400]
label_OrderN = ['<100','(100,200)','(200-300)', '(300-400)','(>400)']
df_ori['OrderN_group'] = pd.cut(df_ori['Order Count'], bins=bin_OrderN, labels=label_OrderN, right=False)
#df_ori['OrderN_group'] = df_ori['OrderN_group'].cat.add_categories('unknown').fillna('unknown')  
 
with col11:  
  with st.expander("Data view"): 
      st.write("""
        Please select which **hour** data you want to view. 
        """)
      allHours=df_ori['Hour'].drop_duplicates()
      default_hour=['All']
      default_hour.extend(state_1)
      hour_choice=st.multiselect("", default_hour)
      if ('All' in hour_choice):
        df_ori_1=df_ori
      else:
        df_ori_1=df_ori.query("hour in @hour_choice")
      st.dataframe(df_ori_1)
         
# Filters
df_1=df_ori
st.sidebar.markdown("## Define **filters:**")
netSales_1, netSales_2 = st.sidebar.slider("Net Sales: ", min(df_ori.Net_Sales), max(df_ori.Net_Sales), (min(df_ori.Net_Sales), max(df_ori.Net_Sales)))
df_1=df_1.query("Net_Sales>=@netSales_1 and Net_Sales<=@netSales_2")
hour_1, hour_2 = st.sidebar.slider("which hour data to be shown",  min(df_ori.Hour), max(df_ori.Hour), (min(df_ori.Hour), max(df_ori.Hour)))    
df_1=df_1.query("Hour>=@hour_1 and Hour<=@hour_2")
orderN_1, orderN_2 = st.sidebar.slider("Order Counts",  min(df_ori.Order_Counts), max(df_ori.Order_Counts), (min(df_ori.Order_Counts), max(df_ori.Order_Counts)))    
df_1=df_1.query("Order_Counts>=@orderN_1 and Order_Counts<=@orderN_2")
#sex=df_1['gender'].drop_duplicates()
#mode=df_1['home_computer'].drop_duplicates()
orderN_choice = st.sidebar.selectbox('Select the range of order counts:', ['All', '<100','(100,200)','(200-300)', '(300-400)','(>400)'])
if orderN_choice != "All":
  df_1=df_1.query("OrderN_group==@orderN_choice")
month_choice = st.sidebar.radio('Whether take the test at home:', ['All', 'Jan.', 'Feb.', 'Mar.'])
if month_choice != "All":
  df_1=df_1.query("Month==@month_choice")


# figures display
#rt_diff = (df_1["rt_total"].max() - df_1["rt_total"].min()) / 10
#df_1["rt_scale"] = (df_1["rt_total"] - df_1["rt_total"].min()) / rt_diff + 1
#df_1["rt_scale"] = pow(df_1["rt_scale"],2)
with col11:  
  title_ch1='Data Visualizaion'
  st.markdown(f'<h3 style="text-aligh: center;color: green;">{title_ch1}</h3>',unsafe_allow_html=True)
  title_ch2='****2D interactive plots********'
  st.markdown(f'<h4 style="text-aligh: center;color: green;">{title_ch2}</h4>',unsafe_allow_html=True)
  with st.expander("Histogram:   distributions of sum score for male/female, under different test-taking mode: take the test at home or not "):    
    fig_hist1=px.histogram(df_1, x='sum_score', color='gender', facet_col='home_computer', marginal='box')
    st.plotly_chart(fig_hist1,  use_container_width=True, height=600)
  with st.expander("Bar charts:    sum score distribution for each age group"): 
    sorted_df = df_1.sort_values(by='age')
    sorted_df = sorted_df.reset_index(drop=True)
    opac = st.text_input('Opacity(0-1)', '0.8')
    fig_bar1=px.bar(sorted_df, y='sum_score', color='age_group', facet_row='age_group', opacity=float(opac), facet_row_spacing=0.01)
    st.plotly_chart(fig_bar1, use_container_width=True, height=400)
  with st.expander("Animation:    display the sum score pattern across states and the relationship with age"):  
    fig_ani1=px.bar(df_1, x='age_group', animation_frame='state_abbr', color='gender')
    fig_ani1.update_layout(transition = {'duration': 30000})
    st.plotly_chart(fig_ani1,  use_container_width=True, height=600)
    fig_ani2=px.scatter(df_1, y='sum_score', x='age', animation_frame='state_abbr', color='gender', size='rt_scale', size_max=60)
    fig_ani2.update_layout(transition = {'duration': 30000})
    st.plotly_chart(fig_ani2,  use_container_width=True, height=600)   
  with st.expander("Pie Charts:    check sum score distribution under country and state"):    
    fig_3=px.sunburst(df_1, color='sum_score',  path=['country_abbr','state_abbr'])
    st.plotly_chart(fig_3,   use_container_width=True, height=600)
  with st.expander("Tree Map:    check total response time distribution under country and state"):    
    fig_tree=px.treemap(df_1, color='rt_total',  path=['country_abbr','state_abbr'])
    st.plotly_chart(fig_tree, use_container_width=True, height=600)    
  with st.expander("choropleth map:    check score distribution from a choropleth map"):
    mean_df = df_1.groupby("country_abbr").mean()
    mean_df.reset_index(inplace=True)
    mean_df = mean_df.rename(columns = {'index':'country_abbr'})
    fig_4=px.choropleth(mean_df, color='sum_score',  locations='country_abbr', locationmode='ISO-3')
    st.plotly_chart(fig_4,  use_container_width=True, height=600)
  title_ch3='****3D interactive plots********'
  st.markdown(f'<h4 style="text-aligh: center;color: green;">{title_ch3}</h4>',unsafe_allow_html=True)
  with st.expander("Check the relationship between total score, age, and test-taking mode (home taking or not) in an interactive 3D way"): 
    fig_scatter1=px.scatter_3d(df_1, y='sum_score', x='age', z='home_computer', color='gender', size='rt_scale', size_max=50)
    st.plotly_chart(fig_scatter1,  use_container_width=True, height=3000)
