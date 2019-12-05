"""
Source:  https://realpython.com/async-io-python/
"""

import asyncio
import time

async def count():
	print('Count 1')
	await asyncio.sleep(0.4)
	print('Count 2')


async def main():
	await asyncio.gather(count(), count(), count())


if __name__ == '__main__':
	s = time.perf_counter()
	asyncio.run(main())
	elapsed = time.perf_counter() - s
	print(f'{__file__} executed in {elapsed:0.2f} seconds')