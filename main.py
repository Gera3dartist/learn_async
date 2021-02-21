import asyncio

async def task1():
	print('started task 1')
	await asyncio.sleep(0)
	print('context switch to task1')


async def task2():
	print('started task 2')
	await asyncio.sleep(0)
	print('context switch to task 2')


async def main():
	tasks = [task1(), task2()]
	await asyncio.gather(*tasks)


asyncio.run(main())