import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as ws:
        print("Connected to server\n")
        try:
            async for message in ws:
                print(f"\n{message}")
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed cleanly.")
        except websockets.exceptions.ConnectionClosedError as e:
            print("Connection closed with error:", e)


async def main():
    try:
        await test_ws()
    except asyncio.CancelledError:
        print(" Connection closed cleanly.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting gracefully...")
