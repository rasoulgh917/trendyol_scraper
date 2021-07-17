import asyncio
from time import sleep


# async def f():
#     await asyncio.sleep(2)
#     print(1)

# async def g():
#     print("g:1")
#     await f()
#     print("g:finish")

# async def e():
#     sleep(3)
#     print('e:between')

# async def main():
#     await asyncio.gather(g(), e())

# asyncio.run(main())

async def tst(i):
    await asyncio.sleep(i)
    return 12

async def c(i):
    print(1)
    b = await tst(i); print(b)
    return 1
async def main():
    print("waiting")
    await asyncio.gather(c(3), c(1), c(1))

asyncio.run(main())