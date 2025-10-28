from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json
import websockets
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(binance_listener())
    print("Server started!")
    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Binance listener stopped")

app = FastAPI(lifespan=lifespan)

latest_data = {}

active_connections = set()

WSS_URI = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

async def binance_listener():
    while True:
        try:
            async with websockets.connect(WSS_URI, ping_interval=20, ping_timeout=60) as ws:
                print("Connected to binance")

                async for message in ws:
                    data = json.loads(message)

                    latest_data["symbol"] = data.get("s")
                    latest_data["price"] = data.get("c")
                    latest_data["change_percent"] = data.get("P")
                    latest_data["timestamp"] = data.get("E")

                    # print(f"{latest_data['symbol']}: ${latest_data['price']}")

                    await broadcast(latest_data)

        except websockets.ConnectionClosed:
            print("Binance connection closed, reconnecting in 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error in Binance listener: {e}")
            await asyncio.sleep(5)

async def broadcast(data):
    if not active_connections:
        return
    
    message = json.dumps(data)
    disconnected = set()

    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            disconnected.add(connection)
    
    active_connections.difference_update(disconnected)

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() #  accept new clients
    active_connections.add(websocket) # save those connections
    print(f"new client connected! Total clients: {len(active_connections)}")

    try:
        while True:
            await websocket.receive_text() # keep receiving from the binance listener
    except WebSocketDisconnect:
        active_connections.discard(websocket)
        print(f"Client disconnected. Total clients: {len(active_connections)}")
    except Exception as e:
        active_connections.discard(websocket)
        print(f"Error: {e}")