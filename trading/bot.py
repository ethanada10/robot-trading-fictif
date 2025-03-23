# === bot.py ===
import datetime
import pandas as pd
from trading.portefeuille import charger_portefeuille, sauvegarder_portefeuille, enregistrer_trade
from trading.data import get_data


def run_trading_bot(ticker):
    portefeuille = charger_portefeuille()
    df = get_data(ticker)

    if df is None or df.empty:
        return "Erreur : données indisponibles."

    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df = df.dropna()  # Supprime les lignes avec NaN (important pour SMA)

    latest = df.iloc[-1]

    signal = "HOLD"
    if float(latest['SMA20']) > float(latest['SMA50']):
        signal = "BUY"
    elif float(latest['SMA20']) < float(latest['SMA50']):
        signal = "SELL"

    # Gestion de la date robustement
    date = latest['Date'] if 'Date' in latest else datetime.datetime.today()
    if isinstance(date, pd.Timestamp):
        date = date.strftime("%Y-%m-%d")
    else:
        date = datetime.datetime.today().strftime("%Y-%m-%d")

    prix = latest['Close']
    position = portefeuille['position']
    actif = portefeuille['actif']

    if signal == "BUY" and position == 0:
        # Achat
        portefeuille['position'] = portefeuille['capital'] / prix
        portefeuille['capital'] = 0
        portefeuille['actif'] = ticker
        enregistrer_trade(date, ticker, "BUY", prix, portefeuille['position'], 0)
        sauvegarder_portefeuille(portefeuille)
        return f"✅ Achat de {ticker} à {prix:.2f} le {date}"

    elif signal == "SELL" and position > 0 and actif == ticker:
        # Vente
        portefeuille['capital'] = position * prix
        portefeuille['position'] = 0
        enregistrer_trade(date, ticker, "SELL", prix, 0, portefeuille['capital'])
        sauvegarder_portefeuille(portefeuille)
        return f"✅ Vente de {ticker} à {prix:.2f} le {date}"

    else:
        return f"⏸️ Aucune action prise aujourd'hui ({signal})"
