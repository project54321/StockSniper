import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import date, timedelta
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

st.set_page_config(page_title="Stock Dashboard", icon = "📊", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <link rel="manifest" href="site.webmanifest">
    <link rel="icon" type="image/png" href="static/android-chrome-192x192.png">
    """,
    unsafe_allow_html=True
)

load_dotenv()

default_ticker = "AAPL"
default_start = date.today() - timedelta(days=30)
default_end = date.today() - timedelta(days=1)

st.title("📊 Stock Dashboard")

col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    ticker = st.text_input("Ticker", value=default_ticker)
with col2:
    start_date = st.date_input("Start Date", value=default_start)
with col3:
    end_date = st.date_input("End Date", value=default_end)

data = pd.DataFrame()
if ticker:
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = [f"{col[0]} {col[1]}" for col in data.columns]

close_col = next((col for col in data.columns if "Close" in col), None)

st.subheader("Raw Data")
st.write(f"Rows: {len(data)}, Columns: {list(data.columns)}")
if not data.empty:
    st.dataframe(data.head())
else:
    st.info("No pricing data available for this ticker/date range.")

if close_col and not data.empty:
    fig = px.line(data, x=data.index, y=close_col, title=f"{ticker} Close Price", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No Close price column found for plotting.")

pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

with pricing_data:
    st.header("Price Movements")
    if close_col and not data.empty:
        df2 = data.copy()
        df2["% Change"] = df2[close_col].pct_change()
        df2.dropna(inplace=True)

        with st.expander("View Detailed Price Data"):
            st.write(df2)

        col_a, col_b, col_c = st.columns(3)
        annual_return = df2["% Change"].mean() * 252 * 100
        stdev = np.std(df2["% Change"]) * np.sqrt(252)
        risk_adj = annual_return / (stdev*100) if stdev > 0 else None

        col_a.metric("Annual Return", f"{annual_return:.2f}%")
        col_b.metric("Volatility", f"{stdev*100:.2f}%")
        col_c.metric("Risk-Adjusted Return", f"{risk_adj:.2f}" if risk_adj else "N/A")
    else:
        st.info("No pricing data to display here.")

with fundamental_data:
    st.header("Fundamental Data")
    key = os.getenv("API_KEY")
    fd = FundamentalData(key, output_format="pandas")

    try:
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        with st.expander("Balance Sheet"):
            st.write(bs)
    except Exception as e:
        st.warning(f"Could not load balance sheet: {e}")

    try:
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        with st.expander("Income Statement"):
            st.write(is1)
    except Exception as e:
        st.warning(f"Could not load income statement: {e}")

    try:
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        with st.expander("Cash Flow Statement"):
            st.write(cf)
    except Exception as e:
        st.warning(f"Could not load cash flow: {e}")

with news:
    st.header(f"News of {ticker}")
    try:
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()
        for i in range(min(10, len(df_news))):
            with st.expander(f"News {i+1}: {df_news['title'][i]}"):
                st.write(df_news["published"][i])
                st.write(df_news["summary"][i])
                st.write(f"Title Sentiment: {df_news['sentiment_title'][i]}")
                st.write(f"News Sentiment: {df_news['sentiment_summary'][i]}")
    except Exception as e:
        st.warning(f"Could not load news: {e}")

st.markdown(
    """
    <hr>
    <p style='text-align:center; font-size:14px; color:gray;'>
    Made by Arjun Averineni | <a href="https://github.com/project54321" target="_blank">GitHub</a>
    </p>
    """,
    unsafe_allow_html=True
)
