import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")

st.title("🚀 Nifty 50 Pro Screener & Exit Tracker")
st.write("આ એપ વિદેશી ફંડોની સ્માર્ટ પદ્ધતિનો ઉપયોગ કરીને આપણા **ભારતીય માર્કેટ (Nifty 50)** નું સચોટ એનાલિસિસ કરે છે.")

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
                
            name = info.get('shortName', ticker)
            div_yield = (info.get('dividendYield', 0) or 0) * 100
            roe = (info.get('returnOnEquity', 0) or 0) * 100
            debt_equity = (info.get('debtToEquity', 0) or 0) / 100
            
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            dma_200 = info.get('twoHundredDayAverage', 0)
            dma_50 = info.get('fiftyDayAverage', 0)
            target_price = info.get('targetMeanPrice', current_price)
            
            upside = 0
            if target_price and current_price and target_price > current_price:
                upside = ((target_price - current_price) / current_price) * 100

            # એક્ઝિટ અને બાય માટેનું ઓટોમેટિક એલર્ટ 
            if current_price >= target_price and target_price > 0:
                action = "🔴 Sell (Target Hit)"
            elif current_price < dma_200:
                action = "🔴 Exit (Downtrend)"
            elif current_price <= dma_50 * 1.05 and current_price >= dma_200:
                action = "🟢 Best Buy Zone"
            else:
                action = "🟡 Hold"

            data.append({
                "Company": name,
                "Symbol": ticker,
                "Action (Alert)": action,
                "Price (₹)": round(current_price, 2),
                "Buy Zone (₹)": round(dma_50, 2),
                "Target (₹)": round(target_price, 2),
                "Upside %": round(upside, 2),
                "200 DMA (₹)": round(dma_200, 2),
                "Dividend %": round(div_yield, 2),
                "ROE %": round(roe, 2),
                "Debt": round(debt_equity, 2)
            })
        except Exception as e:
            pass
            
    if not data:
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    # અહીં આપણે કોલમને હંમેશ માટે ફિક્સ (Lock) કરી દીધા છે!
    cols = ["Company", "Symbol", "Action (Alert)", "Price (₹)", "Buy Zone (₹)", "Target (₹)", "Upside %", "200 DMA (₹)", "Dividend %", "ROE %", "Debt"]
    return df[cols]

st.write("માર્કેટમાંથી Nifty 50 નો લાઈવ ડેટા ખેંચી રહ્યા છીએ... ⏳")
df = get_pro_stock_data(nifty_50)

if not df.empty:
    st.write("---")
    st.subheader("✅ ૧. બેસ્ટ રોકાણ (નવા શેર કયા લેવા?)")
    st.write("શરત: જે નિફ્ટીના શેરો અપટ્રેન્ડ (200 DMA ની ઉપર) માં છે અને તેમાં ભવિષ્યમાં સારો નફો (Upside) મળવાની શક્યતા છે.")
    
    # નવી પ્રેક્ટિકલ શરતો (બેન્કોને પણ ગણતરીમાં લેશે)
    filtered_df = df[
        (df["Price (₹)"] > df["200 DMA (₹)"]) & 
        (df["Upside %"] > 5.0) & 
        (df["ROE %"] > 10.0)
    ].sort_values(by="Upside %", ascending=False)
    
    if not filtered_df.empty:
        st.dataframe(filtered_df.style.format(precision=2), hide_index=True)
    else:
        st.warning("અત્યારે માર્કેટમાં નવા રોકાણ માટે યોગ્ય શેર મળી રહ્યા નથી.")

    st.write("---")
    st.subheader("📊 ૨. એક્ઝિટ ટ્રેકર: Nifty 50 ના તમામ શેરોનું સ્ટેટસ")
    st.write("**Action કોલમ જુઓ:** નવો શેર 'Best Buy Zone' માં લેવો, અને 'Sell' કે 'Exit' આવે ત્યારે વેચી દેવો.")
    st.dataframe(df.style.format(precision=2), hide_index=True)

else:
    st.error("સર્વર કનેક્શનમાં વિલંબ. કૃપા કરીને થોડીવાર પછી પેજ રિફ્રેશ કરો.")
            
