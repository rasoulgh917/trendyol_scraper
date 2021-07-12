import asyncio
from time import sleep

async def sl():
    sleep(3)

async def f():
    await sl()

async def g():
    print("g:1")
    await f()
    print("g:finish")

async def e():
    print('e:between')

async def main():
    await asyncio.gather(g(), g(), e())

asyncio.run(main())