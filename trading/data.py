# === data.py ===
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from trading.indicateurs import ajouter_tous_les_indicateurs


def get_data(ticker):
    end = datetime.today()
    start = end - timedelta(days=100)
    try:
        df = yf.download(ticker, start=start, end=end)
        df.reset_index(inplace=True)
        df = ajouter_tous_les_indicateurs(df)
        return df
    except Exception as e:
        print(f"Erreur récupération données pour {ticker} : {e}")
        return None

