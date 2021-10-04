import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8888") as websocket:
        for x in list(range(10,100,10)):
            await websocket.send(str(x))
        #await websocket.recv()

asyncio.run(hello())
