from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Server: Client connected!")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Server: Message received from client: {data}")
            await websocket.send_text(f"Server: Message received")
    except WebSocketDisconnect:
        print("Server: client disconnected")
    except Exception as e:
        print(f"Server: Error= {e}")