import asyncio
import json
import websockets

WSS_URI = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

async def btcusdt_listener():
    async with websockets.connect(WSS_URI, ping_interval=20, ping_timeout=60) as ws:
        print("connected to binance")

        try:
            async for message in ws:
                data = json.loads(message)
                print(data)
        except websockets.ConnectionClosed:
            print("Connection closed")

asyncio.run(btcusdt_listener())