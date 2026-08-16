import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide") # એપને ફૂલ સ્ક્રીનમાં જોવા માટે

st.title("🚀 Pro Stock Screener: Analysis & Targets")
st.write("આ એડવાન્સ એપ ફંડામેન્ટલ, ટેકનિકલ અને એક્સપર્ટ એનાલિસિસ ભેગું કરીને તમને ક્યારે અને કયા ભાવે શેર લેવો તેનું માર્ગદર્શન આપે છે.")

# નિફ્ટીના કેટલાક શેર્સ (તમે તમારી રીતે વધારી શકો છો)
nifty_tickers = ["TCS.NS", "RELIANCE.NS", "ITC.NS", "INFY.NS", "HDFCBANK.NS", "HINDUNILVR.NS", "SBIN.NS", "ONGC.NS", "COALINDIA.NS", "TATASTEEL.NS", "TATAMOTORS.NS"]

@st.cache_data
def get_pro_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info or 'shortName' not in info:
                continue
                
            name = info.get('shortName', ticker)
            
            # ફંડામેન્ટલ્સ
            div_yield = info.get('dividendYield', 0)
            div_yield = div_yield * 100 if div_yield else 0
            roe = info.get('returnOnEquity', 0)
            roe = roe * 100 if roe else 0
            debt_equity = info.get('debtToEquity', 0)
            debt_equity = debt_equity / 100 if debt_equity else 0
            
            # કિંમત અને ટેકનિકલ લેવલ
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            dma_200 = info.get('twoHundredDayAverage', 0)
            dma_50 = info.get('fiftyDayAverage', 0) # Buy Zone માટે
            
            # ટાર્ગેટ અને રેટિંગ
            target_price = info.get('targetMeanPrice', current_price)
            rating = info.get('recommendationKey', 'N/A').upper()
            
            # કેટલા ટકા નફો મળી શકે? (Upside Potential)
            upside = 0
            if target_price and current_price and target_price > current_price:
                upside = ((target_price - current_price) / current_price) * 100

            data.append({
                "Company": name,
                "Symbol": ticker,
                "Price (₹)": round(current_price, 2),
                "Buy Zone (₹)": round(dma_50, 2),
                "Target (₹)": round(target_price, 2),
                "Upside %": round(upside, 2),
                "Rating": rating,
                "200 DMA (₹)": round(dma_200, 2),
                "Dividend %": round(div_yield, 2),
                "ROE %": round(roe, 2),
                "Debt": round(debt_equity, 2)
            })
        except Exception as e:
            pass
            
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

st.write("માર્કેટમાંથી લાઈવ ડેટા અને એક્સપર્ટ ટાર્ગેટ્સ ખેંચી રહ્યા છીએ... ⏳")
df = get_pro_stock_data(nifty_tickers)

st.write("---")
st.subheader("🎯 પ્રોફેશનલ પિક્સ: કયો શેર, ક્યારે અને કેટલા ટાર્ગેટ માટે લેવો?")
st.write("અહીં એવા જ શેર્સ છે જે ફંડામેન્ટલી મજબૂત છે (ડિવિડન્ડ > 1.5%, ROE > 15%, દેવું < 0.5) અને અપટ્રેન્ડમાં છે.")

if not df.empty:
    # આપણું જૂનું ફિલ્ટર
    filtered_df = df[
        (df["Dividend %"] > 1.5) & 
        (df["ROE %"] > 15.0) & 
        (df["Debt"] < 0.5) &
        (df["Price (₹)"] > df["200 DMA (₹)"])
    ]
    
    if not filtered_df.empty:
        # સારા દેખાવ માટે ડેટાને નફા (Upside %) મુજબ ગોઠવીએ
        filtered_df = filtered_df.sort_values(by="Upside %", ascending=False)
        
        # ઇન્ડેક્સ (આગળના નંબરો) કાઢીને સુંદર ટેબલ બતાવીએ
        st.dataframe(filtered_df.style.format(precision=2), hide_index=True)
        
        st.success("✅ **કેવી રીતે વાંચવું?** જો 'Price' એ 'Buy Zone' ની નજીક હોય, તો તે ખરીદવાનો શ્રેષ્ઠ સમય છે. 'Target' એ આવતા ૧ વર્ષનો અંદાજિત ભાવ છે.")
    else:
        st.warning("અત્યારે માર્કેટમાં આપણી કડક શરતો પાસ કરે અને સારા ટાર્ગેટ આપતી હોય તેવી કોઈ કંપની નથી.")
else:
    st.error("સર્વર કનેક્શનમાં વિલંબ. કૃપા કરીને થોડીવાર પછી પેજ રિફ્રેશ કરો.")
