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
async def c(i):
    print(1)
    await asyncio.sleep(0.1)
    print(2)
    return 1
loop = asyncio.get_event_loop()
l=[1,2,3,4,5]
for i in l:
    asyncio.ensure_future(c(i))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
#print(*[c(i) for i in l])