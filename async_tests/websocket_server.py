import asyncio
import websockets

async def set_backlight(value):
    print(value)

async def reciever(websocket, path):
    async for message in websocket:
        #set_backlitht_to = await websocket.recv()
        await set_backlight(message)
    #print(f"<<< {set_backlitht_to}")
    

async def main():
    async with websockets.serve(reciever, "localhost", 8888):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
