#!/usr/bin/env python

import asyncio
from websockets import serve
from subprocess import Popen, PIPE
from time import sleep

#q = asyncio.LifoQueue()

#await set_backlight(set_backlitht_to)

async def set_backlight(value):
    process_set = Popen(
        ['ddcutil', 'set', '10', value, '--sleep-multiplier', str('.03')],
        stdout=PIPE,
        stderr=PIPE)
    #asyncio.sleep(1)
    stdout, stderr = process_set.communicate()
 

tasks = []
async def reciever(websocket, path):
    #async for message in websocket:
        #print(message)
        #pass
    backlight_value = await websocket.recv()
    await set_backlight(backlight_value)
    #task = asyncio.create_task(backlight_value)
    #tasks.append(task)

async def main():
    async with serve(reciever, "localhost", 8888):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
