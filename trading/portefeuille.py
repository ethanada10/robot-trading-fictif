# === portefeuille.py ===
import json
import os
import pandas as pd

fichier_portefeuille = "data/portefeuille.json"
fichier_trades = "data/trades.csv"


def initialiser_portefeuille():
    portefeuille = {
        "capital": 10000.0,
        "position": 0.0,
        "actif": ""
    }
    sauvegarder_portefeuille(portefeuille)
    if not os.path.exists(fichier_trades):
        pd.DataFrame(columns=["date", "ticker", "type", "prix", "quantite", "capital"]).to_csv(fichier_trades, index=False)
    return portefeuille


def charger_portefeuille():
    if not os.path.exists(fichier_portefeuille):
        return initialiser_portefeuille()
    with open(fichier_portefeuille, "r") as f:
        return json.load(f)


def sauvegarder_portefeuille(p):
    with open(fichier_portefeuille, "w") as f:
        json.dump(p, f)


def enregistrer_trade(date, ticker, type_op, prix, quantite, capital):
    df = pd.read_csv(fichier_trades)
    new_trade = pd.DataFrame.from_dict({
        "date": [date],
        "ticker": [ticker],
        "type": [type_op],
        "prix": [prix],
        "quantite": [quantite],
        "capital": [capital]
    })
    df = pd.concat([df, new_trade], ignore_index=True)
    df.to_csv(fichier_trades, index=False)


def get_portefeuille():
    return charger_portefeuille()


def get_historique():
    if not os.path.exists(fichier_trades):
        return pd.DataFrame(columns=["date", "ticker", "type", "prix", "quantite", "capital"])
    return pd.read_csv(fichier_trades)
