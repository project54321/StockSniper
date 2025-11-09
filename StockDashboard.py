import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import date, timedelta
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

default_ticker = "AAPL"
default_start = date.today() - timedelta(days=30)
default_end = date.today() - timedelta(days=1)

st.title("📊 Stock Dashboard")

ticker = st.sidebar.text_input("Ticker", value=default_ticker)
start_date = st.sidebar.date_input("Start Date", value=default_start)
end_date = st.sidebar.date_input("End Date", value=default_end)

data = pd.DataFrame()
if ticker:
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = [f"{col[0]} {col[1]}" for col in data.columns]

close_col = None
for col in data.columns:
    if "Close" in col:
        close_col = col
        break

st.subheader("Raw Data")
st.write(f"Rows: {len(data)}, Columns: {list(data.columns)}")
if not data.empty:
    st.dataframe(data.head())
else:
    st.info("No pricing data available for this ticker/date range.")

if close_col and not data.empty:
    fig = px.line(data, x=data.index, y=close_col, title=f"{ticker} Close Price")
    st.plotly_chart(fig)
else:
    st.warning("No Close price column found for plotting.")

pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

with pricing_data:
    st.header("Price Movements")
    if close_col and not data.empty:
        df2 = data.copy()
        df2["% Change"] = df2[close_col].pct_change()
        df2.dropna(inplace=True)
        st.write(df2)

        annual_return = df2["% Change"].mean() * 252 * 100
        st.write(f"Annual Return: {annual_return:.2f}%")

        stdev = np.std(df2["% Change"]) * np.sqrt(252)
        st.write(f"Standard Deviation: {stdev*100:.2f}%")

        if stdev > 0:
            st.write(f"Risk-Adjusted Return: {annual_return / (stdev*100):.2f}")
        else:
            st.write("Risk-Adjusted Return: N/A (zero volatility)")
    else:
        st.info("No pricing data to display here.")

with fundamental_data:
    st.header("Fundamental Data")
    key = "TW5N7JYESK82JKWC"
    fd = FundamentalData(key, output_format="pandas")

    try:
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        st.subheader("Balance Sheet")
        st.write(bs)
    except Exception as e:
        st.warning(f"Could not load balance sheet: {e}")

    try:
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        st.subheader("Income Statement")
        st.write(is1)
    except Exception as e:
        st.warning(f"Could not load income statement: {e}")

    try:
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        st.subheader("Cash Flow Statement")
        st.write(cf)
    except Exception as e:
        st.warning(f"Could not load cash flow: {e}")

with news:
    st.header(f"News of {ticker}")
    try:
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()
        for i in range(min(10, len(df_news))):
            st.subheader(f"News {i+1}")
            st.write(df_news["published"][i])
            st.write(df_news["title"][i])
            st.write(df_news["summary"][i])
            st.write(f"Title Sentiment: {df_news['sentiment_title'][i]}")
            st.write(f"News Sentiment: {df_news['sentiment_summary'][i]}")
    except Exception as e:
        st.warning(f"Could not load news: {e}")
