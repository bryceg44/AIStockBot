import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_fetcher import fetch_stock_data
from utils.data_processor import add_technical_indicators
import joblib
import os

# Load the trained model
MODEL_PATH = os.path.join('models', 'stock_model.pkl')
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    st.error("Model not found. Please train the model first.")
    st.stop()

st.title("AI Stock Analyzer")

# Sidebar for user inputs
st.sidebar.header("User Input")
symbol = st.sidebar.text_input("Stock Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

if start_date > end_date:
    st.sidebar.error("Error: End date must fall after start date.")

# Fetch data
data_load_state = st.text('Loading data...')
data = fetch_stock_data(symbol, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
if data is not None:
    data = add_technical_indicators(data)
    data_load_state.text('Loading data...done!')
else:
    st.error("Failed to load data.")
    st.stop()

# Display raw data
if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(data)

# Plot Candlestick Chart
st.subheader(f'{symbol} Price Chart')
fig = go.Figure(data=[go.Candlestick(
    x=data['date'],
    open=data['open'],
    high=data['high'],
    low=data['low'],
    close=data['close'],
    name='Candlestick'
)])

# Add EMAs
fig.add_trace(go.Scatter(x=data['date'], y=data['ema_20'], line=dict(color='blue', width=1), name='EMA 20'))
fig.add_trace(go.Scatter(x=data['date'], y=data['ema_50'], line=dict(color='red', width=1), name='EMA 50'))

fig.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig)

# Predict Next Day's Price
last_row = data.iloc[-1]
features = ['ema_20', 'ema_50', 'rsi', 'macd', 'macdsignal', 'volume']
input_data = last_row[features].values.reshape(1, -1)
predicted_price = model.predict(input_data)[0]
st.subheader("Predicted Next Day's Close Price")
st.write(f"${predicted_price:.2f}")

# Determine Buy/Sell Recommendation
current_price = last_row['close']
if predicted_price > current_price:
    recommendation = "Buy"
    color = "green"
else:
    recommendation = "Sell"
    color = "red"

st.markdown(f"**Recommendation:** <span style='color:{color}'>{recommendation}</span>", unsafe_allow_html=True)
