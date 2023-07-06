import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader.data as web
import func
from streamlit_lottie import st_lottie
import json
import requests

# animation link https://assets8.lottiefiles.com/packages/lf20_wh4gk3bb.json
st.set_page_config(page_title="CAPM",
                   page_icon="bar_chart",
                   layout='wide')




st.title("Capital Asset Pricing Model")
st.markdown("### :green[Financial model that calculates the expected rate of return for an asset or investment]")
    
url = requests.get("https://assets8.lottiefiles.com/packages/lf20_wh4gk3bb.json")
url_json = dict()
if url.status_code == 200:
    url_json = url.json()
st_lottie(url_json,height=400,speed=0.8)


st.divider()
#Input
col1, col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Choose 4 stocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','MGM']) 
with col2:
    year = st.number_input('Number of years',1,10)
    

# Data 
end = datetime.date.today()
start = datetime.date(datetime.date.today().year-year, datetime.date.today().month,datetime.date.today().day)

SP500 = web.DataReader(['sp500'],'fred',start,end)

stocks_df = pd.DataFrame()
for stock in stocks_list:
    data = yf.download(stock,period= f'{year}y')
    stocks_df[f'{stock}'] = data['Close']

# st.write(stocks_df)
stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns = ['Date','sp500']
stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date'] =  stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])

stocks_df = pd.merge(stocks_df,SP500, on = 'Date', how='inner')

col1,col2 = st.columns([1,1])
with col1:
    st.markdown("### Dataframe tail")
    st.dataframe(stocks_df.tail(),use_container_width=True)
with col2:
    st.markdown("### Dataframe head")
    st.dataframe(stocks_df.head(),use_container_width=True)
st.divider()


col1,col2 = st.columns([1,1])
with col1:
    st.markdown("### Price of all stocks")
    st.plotly_chart(func.interactive_plot(stocks_df))
with col2:
    st.markdown("### Price of all stocks after Normalizing")
    st.plotly_chart(func.interactive_plot(func.normalise(stocks_df)))


stocks_daily_returns = func.daily_returns(stocks_df)

