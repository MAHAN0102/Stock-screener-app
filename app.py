import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚀 Nifty 50 Pro Screener")

nifty_50 = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "INFY.NS", "ITC.NS", "LT.NS", "BAJFINANCE.NS"]

@st.cache_data(ttl=3600)
def get_clean_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # લેટેસ્ટ ભાવ અને ટાર્ગેટ
            curr = info.get('currentPrice', info.get('regularMarketPrice', 0))
            target = info.get('targetMeanPrice', curr)
            dma_50 = info.get('fiftyDayAverage', 0)
            
            # જો ભાવ ખોટો (ખૂબ મોટો) આવે, તો તેને ક્લીન કરો
            if curr > 100000: curr = info.get('regularMarketPrice', 0)
            
            data.append({
                "Company": info.get('shortName', ticker)[:12],
                "Action": "🟢Buy" if curr <= dma_50*1.05 else "🟡Hold",
                "Price": round(curr, 2),
                "Target": round(target, 2)
            })
        except: continue
    return pd.DataFrame(data)

df = get_clean_data(nifty_50)

st.subheader("✅ ૧. સ્ક્રીનર")
st.table(df)
st.subheader("📊 ૨. ટ્રેકર")
st.table(df)
