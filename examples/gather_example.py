"""
Source:  https://realpython.com/async-io-python/
"""

import asyncio
import time


async def simple_coro(name):
	print('Task: fired and forget')
	await asyncio.sleep(0.5)

	return name, len(name)


async def main():
	result = await asyncio.gather(
		simple_coro('foo'),
		simple_coro('bar'),
		simple_coro('baz'),
		simple_coro('barbar'),
		return_exceptions=True
	)
	print(f'got result: {dict(result)}')




if __name__ == '__main__':
	s = time.perf_counter()
	asyncio.run(main())
	elapsed = time.perf_counter() - s
	print(f'{__file__} executed in {elapsed:0.2f} seconds')
