# === indicateurs.py ===
import pandas as pd


def ajouter_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def ajouter_macd(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal_MACD'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram_MACD'] = df['MACD'] - df['Signal_MACD']
    return df


def ajouter_bollinger(df, window=20, nb_std=2):
    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()
    df['Bollinger_High'] = rolling_mean + nb_std * rolling_std
    df['Bollinger_Low'] = rolling_mean - nb_std * rolling_std
    return df


def ajouter_tous_les_indicateurs(df):
    df = ajouter_rsi(df)
    df = ajouter_macd(df)
    df = ajouter_bollinger(df)
    return df