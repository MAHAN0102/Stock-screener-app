import streamlit as st
import yfinance as yf
import pandas as pd

# સ્ક્રીનને પૂરેપૂરી વાપરવા માટે
st.set_page_config(layout="wide")

st.title("🚀 Nifty 50 Pro Screener & Exit Tracker")
st.write("માર્કેટના દરેક શેરનું પ્રોફેશનલ ક્વોન્ટ એનાલિસિસ - લાઈવ")

nifty_50 = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", 
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS", 
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", 
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", 
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS", 
    "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LTIM.NS", 
    "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS", 
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS", 
    "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS", 
    "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]

@st.cache_data(ttl=3600)
def get_pro_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # ડેટા પ્રોસેસિંગ
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            dma_200 = info.get('twoHundredDayAverage', 0)
            dma_50 = info.get('fiftyDayAverage', 0)
            target = info.get('targetMeanPrice', current_price)
            
            # એક્શન લોજિક
            action = "🟡 Hold"
            if current_price >= target and target > 0: action = "🔴 Sell"
            elif current_price < dma_200: action = "🔴 Exit"
            elif current_price <= dma_50 * 1.05: action = "🟢 Buy"

            data.append({
                "Company": info.get('shortName', ticker),
                "Symbol": ticker,
                "Action": action,
                "Price": round(current_price, 2),
                "Target": round(target, 2),
                "Upside%": round(((target-current_price)/current_price)*100, 2) if target > current_price else 0,
                "ROE%": round((info.get('returnOnEquity', 0) or 0) * 100, 2),
                "Debt": round((info.get('debtToEquity', 0) or 0) / 100, 2)
            })
        except: continue
    return pd.DataFrame(data)

# ડેટા લોડિંગ
with st.spinner('માર્કેટ ડેટા ફેચ થઈ રહ્યો છે...'):
    df = get_pro_stock_data(nifty_50)

# ટેબલ દર્શાવવા માટે (ફુલ વિડ્થ સાથે)
if not df.empty:
    st.subheader("📊 Nifty 50 માર્કેટ ડેશબોર્ડ")
    # આ લાઈનથી ટેબલ આખી સ્ક્રીન પર ફેલાઈ જશે
    st.dataframe(df, use_container_width=True, height=600) 
    st.info("💡 ઉપરના ટેબલમાં કોઈપણ હેડર (જેમ કે 'Upside%') પર ક્લિક કરીને તમે શેરોને ગોઠવી શકો છો.")
else:
    st.error("સર્વર બીઝી છે, થોડીવાર પછી રિફ્રેશ કરો.")
