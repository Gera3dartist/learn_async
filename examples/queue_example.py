"""
Reference: https://realpython.com/async-io-python/#the-10000-foot-view-of-async-io

"""

import asyncio
import time
import random
import sys

from asyncio import Queue


class Item:
	__slots__ = ()

	async def do(self):
		print(f'Item ID: {id(self)}')


async def do_tasks_cleanup(tasks):
	for task in tasks:
		task.cancel()
	# Wait until all worker tasks are cancelled.
	await asyncio.gather(*tasks, return_exceptions=True)


async def producer(queue: Queue, counter=100, name='producer'):
	while counter >= 0:
		i = Item()
		await queue.put(i)
		print(f'[{name.upper()}] put {i} in queue')
		await asyncio.sleep(random.randint(0, 2))
		counter -= 1


async def consumer(queue, name):
	print(f'Looping in consumer: {name}')
	while True:
		item = await queue.get()
		print(f'[{name.upper()}] {name} got item: {item}')
		await item.do()
		queue.task_done()


async def main():
	queue = Queue()
	producers = [asyncio.create_task(producer(queue, name=f'Producer-{i}')) for i in range(2)]
	workers = [asyncio.create_task(consumer(queue, f'Consumer-{i}')) for i in range(3)]
	await asyncio.gather(*producers)

	print("wait till last message will be processed by worker")
	await queue.join()
	await do_tasks_cleanup(workers)



if __name__ == '__main__':
	s = time.perf_counter()
	asyncio.run(main(), debug=True)
	elapsed = time.perf_counter() - s
	print(f'{__file__} executed in {elapsed:0.2f} seconds')
