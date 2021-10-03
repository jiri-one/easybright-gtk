#!/usr/bin/env python

from asyncio import Future, run, sleep
from websockets import serve
from subprocess import Popen, PIPE
from time import sleep

async def set_backlight(value):
    process_set = Popen(
        ['ddcutil', 'set', '10', value, '--sleep-multiplier', str('.03')],
        stdout=PIPE,
        stderr=PIPE)
    #sleep(1)
    stdout, stderr = process_set.communicate()

async def reciever(websocket, path):
    set_backlitht_to = await websocket.recv()
    print(f"<<< {set_backlitht_to}")
    await set_backlight(set_backlitht_to)

async def main():
    async with serve(reciever, "localhost", 8888):
        await Future()  # run forever


if __name__ == '__main__':
    run(main())
