# === app.py ===
import streamlit as st
from trading.bot import run_trading_bot
from trading.portefeuille import get_portefeuille, get_historique
from trading.data import get_data
from trading.rapport import generer_pdf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import base64
import os

st.set_page_config(page_title="Robot de Trading Fictif", layout="wide")

# === Fond sombre pour l'app ===
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #1c1e26;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #444444;
        color: #ffffff;
        border: none;
    }
    .stSelectbox>div>div {
        background-color: #222222;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Robot de Trading - Argent Fictif (Actions)")

# Sélection de l'action à trader
asset = st.selectbox("Choisissez une action (Ticker)", ["AAPL", "MSFT", "GOOGL", "AMZN", "META"])

# Charger les données actuelles
df = get_data(asset)

# Afficher graphique prix + Bollinger
st.subheader(f"📈 Graphique de {asset} avec Bollinger Bands")
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close'))
fig_price.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger_High'], name='Bollinger High', line=dict(dash='dot')))
fig_price.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger_Low'], name='Bollinger Low', line=dict(dash='dot')))
fig_price.update_layout(template="plotly_dark")
st.plotly_chart(fig_price, use_container_width=True)

# RSI
st.subheader("📊 RSI (14)")
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI'))
fig_rsi.add_hline(y=70, line_dash="dot", line_color="red")
fig_rsi.add_hline(y=30, line_dash="dot", line_color="green")
fig_rsi.update_layout(template="plotly_dark", yaxis_title="RSI")
st.plotly_chart(fig_rsi, use_container_width=True)

# MACD
st.subheader("📉 MACD")
fig_macd = go.Figure()
fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name='MACD'))
fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['Signal_MACD'], name='Signal'))
fig_macd.add_trace(go.Bar(x=df['Date'], y=df['Histogram_MACD'], name='Histogram'))
fig_macd.update_layout(template="plotly_dark")
st.plotly_chart(fig_macd, use_container_width=True)

# Lancer le bot
if st.button("📈 Lancer le robot de trading aujourd'hui"):
    result = run_trading_bot(asset)
    st.success(result)

# Afficher portefeuille actuel
portefeuille = get_portefeuille()
st.metric("Capital actuel ($)", f"{portefeuille['capital']:.2f}")
st.metric("Position actuelle", f"{portefeuille['position']} {portefeuille['actif'] if portefeuille['position'] > 0 else ''}")

# Afficher historique des trades
st.subheader("📜 Historique des trades")
df_hist = get_historique()
st.dataframe(df_hist.tail(10), use_container_width=True)

# Boutons export CSV / Excel
st.download_button("📤 Télécharger CSV", data=df_hist.to_csv(index=False), file_name="trades.csv", mime="text/csv")

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df_hist.to_excel(writer, index=False, sheet_name='Trades')
    writer.close()
st.download_button("📤 Télécharger Excel", data=buffer.getvalue(), file_name="trades.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Bouton pour générer un rapport PDF
if st.button("📄 Générer le rapport PDF"):
    chemin_pdf = generer_pdf(df_hist, portefeuille)
    with open(chemin_pdf, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="rapport_trading.pdf">📥 Télécharger le rapport PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

# Courbe capital
fig = px.line(df_hist, x="date", y="capital", title="Évolution du capital fictif")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
