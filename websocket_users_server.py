import asyncio
import websockets


async def handler(websocket):
    message = await websocket.recv()
    print(f"Получено сообщение от пользователя: {message}")

    for i in range(1, 6):
        response = f"{i} Сообщение пользователя: {message}"
        await websocket.send(response)


async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    await server.wait_closed()


asyncio.run(main())