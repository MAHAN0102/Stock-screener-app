import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 Long-Term Investment & Dividend Screener")
st.write("આ એપ ઑટોમેટિક નિફ્ટીના શેરોનું એનાલિસિસ કરીને બેસ્ટ ડિવિડન્ડ અને મજબૂત કંપનીઓ શોધે છે.")

nifty_tickers = ["TCS.NS", "RELIANCE.NS", "ITC.NS", "INFY.NS", "HDFCBANK.NS", "HINDUNILVR.NS", "SBIN.NS", "ONGC.NS", "COALINDIA.NS"]

@st.cache_data
def get_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            name = info.get('shortName', ticker)
            div_yield = info.get('dividendYield', 0)
            div_yield = div_yield * 100 if div_yield else 0
            roe = info.get('returnOnEquity', 0)
            roe = roe * 100 if roe else 0
            debt_equity = info.get('debtToEquity', 0)
            debt_equity = debt_equity / 100 if debt_equity else 0
            
            data.append({
                "Company": name,
                "Symbol": ticker,
                "Dividend %": round(div_yield, 2),
                "ROE %": round(roe, 2),
                "Debt": round(debt_equity, 2)
            })
        except Exception as e:
            pass
    return pd.DataFrame(data)

st.write("માર્કેટમાંથી ડેટા લાવી રહ્યા છીએ... (કૃપા કરીને રાહ જુઓ)")
df = get_stock_data(nifty_tickers)

st.write("---")
st.subheader("✅ આપણી શરતો મુજબ પાસ થયેલા બેસ્ટ શેર્સ")
st.write("શરતો: ડિવિડન્ડ 1.5% થી વધુ, ROE 15% થી વધુ, અને દેવું 0.5 થી ઓછું હોવું જોઈએ.")

filtered_df = df[
    (df["Dividend %"] > 1.5) & 
    (df["ROE %"] > 15.0) & 
    (df["Debt"] < 0.5)
]

st.dataframe(filtered_df)

if not filtered_df.empty:
    st.success("🎉 અભિનંદન! આ એવા શેર્સ છે જે નિયમિત ડિવિડન્ડ આપે છે, દેવું ઓછું છે અને નફો સારો છે!")
else:
    st.warning("અત્યારે આ શરતો પાસ કરે તેવી કોઈ કંપની નથી મળી.")
