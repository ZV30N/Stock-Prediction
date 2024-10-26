import yfinance as yf
from prophet import Prophet
import pandas as pd
from plotly import graph_objs as go
from datetime import date

START = "2015-01-01"
END = date.today().strftime("%Y-%m-%d")

# Function to download stock data
def download_data(stock, start=START, end=END):
    data = yf.download(stock, start, end)
    data.reset_index(inplace=True)
    data = data.dropna()
    return data

# Function to predict stock prices
def predict_stock(data, period):
    df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet()
    model.fit(df_train)

    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)
    return forecast

# Function to prepare plot
def prepare_plot(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text='Time Series Analysis', xaxis_rangeslider_visible=True)
    return fig

# Function to get ticker information (company name, etc.)
def get_ticker_info(stock_ticker):
    ticker_info = yf.Ticker(stock_ticker).info
    company_name = ticker_info.get('longName', stock_ticker)
    return company_name
