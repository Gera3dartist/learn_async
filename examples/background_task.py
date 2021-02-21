"""
Source:  https://realpython.com/async-io-python/
"""

import asyncio
import time


async def task():
	print('Task: fired and forget')
	await asyncio.sleep(1)
	print('Task DONE')


async def handler():
	await asyncio.sleep(0.2)
	print('>>>[handler] running before task')
	asyncio.create_task(task())
	await asyncio.sleep(0.2)
	print('>>>[handler]  running  after task')


async def main():
	await handler()
	print('sleep in main....')
	await asyncio.sleep(1)



if __name__ == '__main__':
	s = time.perf_counter()
	asyncio.run(main())
	elapsed = time.perf_counter() - s
	print(f'{__file__} executed in {elapsed:0.2f} seconds')
