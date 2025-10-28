import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws"

    try:
        async with websockets.connect(uri) as ws:
            print("Client: Connected to server")

            try:
                while True:
                    response = await ws.recv()
                    print(f"\n{response}")
            except websockets.exceptions.ConnectionClosed:
                pass

            except KeyboardInterrupt:
                print(f"\nClient: Interrupted by user")

            finally:
                await ws.close()

    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed cleanly")
    except websockets.exceptions.ConnectionClosedError as e:
        print("Connection closed with error:", e)
    except Exception as e:
        print("Other error:", e)

asyncio.run(test_ws())