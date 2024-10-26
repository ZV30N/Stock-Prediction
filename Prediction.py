import pandas as pd

import streamlit as st
from datetime import date, timedelta
from plotly import graph_objs as go
import sys
import yfinance as yf

START = "2015-01-01"
END = date.today().strftime("%Y-%m-%d")


st.title("Stocks Prediction App by Stanley")
stock = 'AAPL'
n_years = st.slider("Years of Prediction : ", 1,4)

period = n_years * 356


# @st.cache_data
def download_data(ticker):
    data = yf.download(stock,START,END)
    data.reset_index(inplace =True)
    return data

data = download_data(stock)

st.subheader('Raw Data')
st.write(data.tail())

def plot_raw():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'], name ='stock_open'), )
    fig.update_traces(line_color = 'red')
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Close'],name = 'stock_close'))
    fig.layout.update(title_text = 'Time Series Analysis', xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

plot_raw()


#forecasting 
data = data.dropna()
# data['MA_10'] = data['Close'].rolling(window=10).mean()   #10 day moving average
# data['MA_50'] = data['Close'].rolling(window=50).mean()   #50 day moving average

from prophet import Prophet
from prophet.plot import plot_plotly

# Prepare the training data for Prophet
df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

# Initialize and fit the Prophet model
model = Prophet()
model.fit(df_train)

# Generate future dates for predictions (based on number of periods)
future = model.make_future_dataframe(periods=period)

# Forecast the future values
forecast = model.predict(future)

# Show forecast data in Streamlit
st.subheader('Forecast Data')
st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Plot the forecast data using Plotly
st.write('Forecast plot')
fig1 = plot_plotly(model,forecast)
st.plotly_chart(fig1)

st.write('Forecast Component')
fig2 = model.plot_components(forecast)
st.write(fig2)


# Trading Strategy
initial_bal = 1000
balance = initial_bal
n_shares = 0






