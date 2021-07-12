import asyncio
from time import sleep


async def f():
    await asyncio.sleep(2)

async def g():
    print("g:1")
    await f()
    print("g:finish")

async def e():
    print('e:between')

async def main():
    await asyncio.gather(g(), e())

asyncio.run(main())