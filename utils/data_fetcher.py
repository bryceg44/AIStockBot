import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

TRADIER_API_KEY = os.getenv('TRADIER_API_KEY')
BASE_URL = 'https://api.tradier.com/v1/markets/history'

def fetch_stock_data(symbol, start_date, end_date, interval='daily'):
    headers = {
        'Authorization': f'Bearer {TRADIER_API_KEY}',
        'Accept': 'application/json'
    }
    params = {
        'symbol': symbol,
        'interval': interval,
        'start': start_date,
        'end': end_date
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'history' in data and 'day' in data['history']:
            df = pd.DataFrame(data['history']['day'])
            # Convert relevant columns to numeric
            df['close'] = pd.to_numeric(df['close'])
            df['open'] = pd.to_numeric(df['open'])
            df['high'] = pd.to_numeric(df['high'])
            df['low'] = pd.to_numeric(df['low'])
            df['volume'] = pd.to_numeric(df['volume'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        else:
            print(f"No data found for symbol: {symbol}")
            return None
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None
