import pandas as pd
import talib

def add_technical_indicators(df):
    # Calculate EMAs
    df['ema_20'] = talib.EMA(df['close'], timeperiod=20)
    df['ema_50'] = talib.EMA(df['close'], timeperiod=50)

    # Calculate RSI
    df['rsi'] = talib.RSI(df['close'], timeperiod=14)

    # Calculate MACD
    macd, macdsignal, macdhist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macdsignal'] = macdsignal
    df['macdhist'] = macdhist

    # Drop rows with NaN values
    df.dropna(inplace=True)

    return df
