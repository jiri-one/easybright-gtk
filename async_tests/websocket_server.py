import asyncio
import websockets
from subprocess import PIPE

running_process = None
next_value = None

async def set_backlight():
    global running_process
    running_process = True
    global next_value
    try:
        while next_value is not None:
            value = next_value
            next_value = None
            process_set = await asyncio.create_subprocess_exec('ddcutil', 'set', '10', value, '--sleep-multiplier', str('.03'), stdout=PIPE, stderr=PIPE)
            stdout, stderr = await process_set.communicate()
    finally:
        running_process = False

async def reciever(websocket, path):
    #set_backlitht_to = await websocket.recv() # another method to recieve message
    async for message in websocket:
        global next_value
        next_value = message
        if not running_process:
            asyncio.create_task(set_backlight())

async def main():
    async with websockets.serve(reciever, "localhost", 8888):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except OSError as e:
        print(e)
        pass    
