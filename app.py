import streamlit as st
import yfinance as yf
import pandas as pd

# સ્ક્રીન સેટિંગ્સ
st.set_page_config(layout="wide")
st.title("🚀 Nifty 50 Pro Screener")

# નિફ્ટી 50 ના શેરો
nifty_50 = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "INFY.NS", "ITC.NS", "LT.NS", "BAJFINANCE.NS"]

@st.cache_data(ttl=3600)
def get_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            curr = info.get('currentPrice', info.get('regularMarketPrice', 0))
            dma_50 = info.get('fiftyDayAverage', 0)
            target = info.get('targetMeanPrice', curr)
            
            # ડેટા ડિક્શનરી
            data.append({
                "Company": info.get('shortName', ticker)[:15],
                "Action": "🟢Buy" if curr <= dma_50*1.05 else "🟡Hold",
                "Price": round(curr, 2),
                "Target": round(target, 2)
            })
        except: continue
    return pd.DataFrame(data)

# ડેટા મેળવો
df = get_data(nifty_50)

# ટેબલ દર્શાવો
st.subheader("✅ ૧. સ્ક્રીનર")
st.table(df)

st.subheader("📊 ૨. ટ્રેકર")
st.table(df)
            
