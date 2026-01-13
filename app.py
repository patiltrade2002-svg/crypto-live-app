import streamlit as st
import asyncio
import threading
import time

from price_engine import PRICES, coinbase_ws

# -----------------------------
# Start WebSocket in background
# -----------------------------
def start_ws():
    asyncio.run(coinbase_ws())

threading.Thread(target=start_ws, daemon=True).start()

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Live Crypto Scanner", layout="wide")
st.title("⚡ Live Crypto Price Scanner (Dexscreener-style)")

st.markdown("Real-time prices from **Coinbase WebSocket**")

table = st.empty()

# -----------------------------
# Live update loop
# -----------------------------
while True:
    if PRICES:
        data = []

        for symbol, p in PRICES.items():
            spread = p["ask"] - p["bid"]
            spread_pct = (spread / p["price"]) * 100

            data.append({
                "Coin": symbol.replace("-USD", ""),
                "Price ($)": round(p["price"], 2),
                "Bid": round(p["bid"], 2),
                "Ask": round(p["ask"], 2),
                "Spread %": round(spread_pct, 4)
            })

        table.table(data)

    else:
        table.info("Waiting for live price feed...")

    time.sleep(1)

