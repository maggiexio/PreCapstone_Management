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
  title_11="Hello! I am Henry. Can I help you?"
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
df_ori=raw_data("./data/Sales_Summary_123_2022_Spokane-Python.xlsx", "Hourly_Breakdown")
df_ori['NetSale_group']=""
df_ori['OrderN_group']=""
df_ori['GuestN_group']=""
bin_OrderN= [0,100,200,300,400, 500]
label_OrderN = ['<100','(100,200)','(200-300)', '(300-400)','(>400)']
df_ori['OrderN_group'] = pd.cut(df_ori['Order_Count'], bins=bin_OrderN, labels=label_OrderN, right=False)
#df_ori['OrderN_group'] = df_ori['OrderN_group'].cat.add_categories('unknown').fillna('unknown')  
 
with col11:  
  with st.expander("Data view"): 
      st.write("""
        Please select which **hour** data you want to view. 
        """)
      allHours=df_ori['Hour'].drop_duplicates()
      default_hour=['All']
      default_hour.extend(allHours)
      hour_choice=st.multiselect("", default_hour)
      if ('All' in hour_choice):
        df_ori_1=df_ori
      else:
        df_ori_1=df_ori.query("Hour in @hour_choice")
      st.dataframe(df_ori_1)
         
# Filters
df_1=df_ori
st.sidebar.markdown("## Define **filters:**")
netSales_1, netSales_2 = st.sidebar.slider("Net Sales: ", min(df_ori.Net_Sales), max(df_ori.Net_Sales), (min(df_ori.Net_Sales), max(df_ori.Net_Sales)))
df_1=df_1.query("Net_Sales>=@netSales_1 and Net_Sales<=@netSales_2")
hour_1, hour_2 = st.sidebar.slider("which hour data to be shown",  min(df_ori.Hour), max(df_ori.Hour), (min(df_ori.Hour), max(df_ori.Hour)))    
df_1=df_1.query("Hour>=@hour_1 and Hour<=@hour_2")
orderN_1, orderN_2 = st.sidebar.slider("Order_Count",  min(df_ori.Order_Count), max(df_ori.Order_Count), (min(df_ori.Order_Count), max(df_ori.Order_Count)))    
df_1=df_1.query("Order_Count>=@orderN_1 and Order_Count<=@orderN_2")
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

  title_ch3='****3D interactive plots********'
  st.markdown(f'<h4 style="text-aligh: center;color: green;">{title_ch3}</h4>',unsafe_allow_html=True)
  with st.expander("Check the relationship between Month, hour and net sales in an interactive 3D way"): 
    fig_scatter1=px.scatter_3d(df_1, y='Net_Sales', x='Hour', z='Month', color='Month', size='Net_Sales', size_max=50)
    st.plotly_chart(fig_scatter1,  use_container_width=True, height=3000)
