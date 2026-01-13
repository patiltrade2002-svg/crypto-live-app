import asyncio
import json
import websockets

# Global price store (in-memory)
PRICES = {}

COINS = ["BTC-USD", "ETH-USD", "SOL-USD"]

async def coinbase_ws():
    uri = "wss://ws-feed.exchange.coinbase.com"

    async with websockets.connect(uri) as ws:
        subscribe_msg = {
            "type": "subscribe",
            "channels": [{
                "name": "ticker",
                "product_ids": COINS
            }]
        }

        await ws.send(json.dumps(subscribe_msg))

        while True:
            msg = json.loads(await ws.recv())

            if msg.get("type") == "ticker":
                symbol = msg["product_id"]
                PRICES[symbol] = {
                    "price": float(msg["price"]),
                    "bid": float(msg["best_bid"]),
                    "ask": float(msg["best_ask"])
                }
