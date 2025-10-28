import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws"

    try:
        async with websockets.connect(uri) as ws:
            print("Client: Connected to server")

            receive_task = asyncio.create_task(receive_messages(ws)) #continuously listen for server msg

            try:
                while True:
                    message = await asyncio.get_event_loop().run_in_executor(None, input, "You: ")

                    if message.lower() == 'quit':
                        print("closing connection")
                        break

                    await ws.send(message)

            except KeyboardInterrupt:
                print("\nClient: Interrupted by user")

            finally:
                receive_task.cancel()
                await ws.close()

    except websockets.exceptions.ConnectionClosedOK:
        print("Client: Connection closed cleanly")
    except websockets.exceptions.ConnectionClosedError as e:
        print("Client: ❌ Connection closed with error:", e)
    except Exception as e:
        print("Client: ⚠️ Other error:", e)

async def receive_messages(ws):
    try:
        while True:
            response = await ws.recv()
            print(f"\Client: {response}")
            print("You: ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        pass

asyncio.run(test_ws())