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
            
            if not info or 'shortName' not in info:
                continue
                
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            dma_200 = info.get('twoHundredDayAverage', 0)
            dma_50 = info.get('fiftyDayAverage', 0)
            target = info.get('targetMeanPrice', current_price)
            
            # એક્શન લોજિક
            action = "🟡 Hold"
            if current_price >= target and target > 0: action = "🔴 Sell"
            elif current_price < dma_200: action = "🔴 Exit"
            elif current_price <= dma_50 * 1.05: action = "🟢 Buy"

            upside = ((target-current_price)/current_price)*100 if target > current_price else 0

            data.append({
                "Company": info.get('shortName', ticker),
                "Symbol": ticker,
                "Action": action,
                "Price": round(current_price, 2),
                "Buy Zone": round(dma_50, 2),
                "Target": round(target, 2),
                "Upside%": round(upside, 2),
                "200 DMA": round(dma_200, 2),
                "Div%": round((info.get('dividendYield', 0) or 0) * 100, 2),
                "ROE%": round((info.get('returnOnEquity', 0) or 0) * 100, 2),
                "Debt": round((info.get('debtToEquity', 0) or 0) / 100, 2)
            })
        except: 
            continue
            
    if data:
        df = pd.DataFrame(data)
        # કોલમને કાયમ માટે અહી ફિક્સ કરી દીધા છે
        cols = ["Company", "Symbol", "Action", "Price", "Buy Zone", "Target", "Upside%", "200 DMA", "Div%", "ROE%", "Debt"]
        return df[cols]
    return pd.DataFrame()

with st.spinner('માર્કેટ ડેટા ફેચ થઈ રહ્યો છે...'):
    df = get_pro_stock_data(nifty_50)

if not df.empty:
    st.write("---")
    st.subheader("✅ ૧. સ્ક્રીનર: અત્યારે કયા નવા શેર લેવા જેવા છે?")
    
    # શરતો
    filtered_df = df[
        (df["Price"] > df["200 DMA"]) & 
        (df["Upside%"] > 5.0) & 
        (df["ROE%"] > 10.0)
    ].sort_values(by="Upside%", ascending=False)
    
    if not filtered_df.empty:
        # hide_index=True થી 0,1,2 નીકળી જશે, use_container_width=True થી મોટું થશે
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.warning("અત્યારે માર્કેટમાં કોઈ નવો શેર લેવા જેવો નથી.")

    st.write("---")
    st.subheader("📊 ૨. એક્ઝિટ ટ્રેકર: Nifty 50 ના તમામ શેરોનું સ્ટેટસ")
    # આ ટેબલ આખી સ્ક્રીન પર લાંબુ દેખાશે
    st.dataframe(df, use_container_width=True, hide_index=True, height=600) 

else:
    st.error("સર્વર બીઝી છે, થોડીવાર પછી રિફ્રેશ કરો.")
        
