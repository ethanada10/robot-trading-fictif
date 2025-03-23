# === rapport.py ===
import pdfkit
import pandas as pd
from datetime import datetime
import os

def generer_pdf(df_trades, portefeuille, nom_fichier="rapport_trading.pdf"):
    # Préparer les données
    date_rapport = datetime.today().strftime("%Y-%m-%d")
    capital = portefeuille.get("capital", 0)
    position = portefeuille.get("position", 0)
    actif = portefeuille.get("actif", "")

    dernier_trade = df_trades.iloc[-1] if not df_trades.empty else None

    # Construire le HTML
    html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Arial; background-color: #f4f4f4; color: #333; padding: 20px; }}
        h1 {{ color: #222; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #999; padding: 8px; text-align: center; }}
        th {{ background-color: #333; color: white; }}
    </style>
    </head>
    <body>
        <h1>📊 Rapport de Trading - {actif}</h1>
        <p><strong>Date :</strong> {date_rapport}</p>
        <p><strong>Capital actuel :</strong> ${capital:.2f}</p>
        <p><strong>Position :</strong> {position} {actif}</p>
        {f'<p><strong>Dernier trade :</strong> {dernier_trade["type"]} à {dernier_trade["prix"]:.2f} le {dernier_trade["date"]}</p>' if dernier_trade is not None else ''}
        <h2>📈 Historique des trades</h2>
        {df_trades.to_html(index=False)}
    </body>
    </html>
    """

    # Créer le PDF
    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
    }

    chemin_sortie = os.path.join("data", nom_fichier)
    pdfkit.from_string(html, chemin_sortie, options=options)
    return chemin_sortie
