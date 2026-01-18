import asyncio
import websockets


async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Привет, сервер!")

        for _ in range(5):
            message = await websocket.recv()
            print(message)


asyncio.run(client())