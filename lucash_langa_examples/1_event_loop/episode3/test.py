import asyncio
from datetime import datetime


async def coro1() -> str:
	await asyncio.sleep(0.2)
	raise RuntimeError('oops bad thing happened')

async def coro2(x) -> int:
	await asyncio.sleep(0.3)
	return x * 2



async def async_main():

	res = await asyncio.gather(
		coro1(),
		coro2(2),
		coro2(0),
		return_exceptions=True
	)
	print(res)



asyncio.run(async_main())
